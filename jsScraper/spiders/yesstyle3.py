import scrapy
import json
import os
import time
from pathlib import Path
from playwright_stealth import stealth_sync

class YesStyleSpider(scrapy.Spider):
    name = "yesstyle_combined"

    start_urls = [
        "https://www.yesstyle.com/en/beauty-eyes/list.html/bcc.15488_bpt.46"
    ]

    custom_settings = {
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": False,
        },
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 5,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_dir = Path("../../data/yesstyle/yesstyle_beauty_eyes")
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.output_file = self.data_dir / "yesstyle_final_output.json"
        self.source_of_truth_file = self.data_dir / "yesstyle_scraped_data.json"
        
        self.scraped_data = self.load_existing_data()  # Load scraped product info if available

    def load_existing_data(self):
        """Load previously scraped data from JSON file."""
        if self.source_of_truth_file.exists():
            with open(self.source_of_truth_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"products": {}}

    def save_source_of_truth(self):
        """Save scraped data to JSON for progress tracking."""
        with open(self.source_of_truth_file, "w", encoding="utf-8") as f:
            json.dump(self.scraped_data, f, indent=4)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_product_list,
                headers=self.headers,
                meta={"playwright": True, "playwright_include_page": True},
            )

    async def parse_product_list(self, response):
        """Parse product listing page and capture product URLs and IDs."""
        page = response.meta["playwright_page"]
        stealth_sync(page)

        current_page = 1
        max_scrolls = 30

        for _ in range(max_scrolls):
            self.log(f"Scraping page {current_page}")
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            await page.wait_for_timeout(5000)

            async with page.expect_response(lambda r: "rest/products/v1/department" in r.url) as resp_info:
                response_api = await resp_info.value
                response_json = await response_api.json()

                # Process products in the JSON response
                self.process_products(response_json)

            current_page += 1

        await page.close()

        # After gathering product URLs, start scraping individual product pages
        for product_id, product_info in self.scraped_data["products"].items():
            if not product_info.get("visited"):  # Skip products already visited
                yield scrapy.Request(
                    url=product_info["url"],
                    callback=self.parse_product_page,
                    meta={"product_id": product_id}
                )

    def process_products(self, response_json):
        """Extract productId and URL from the JSON and save if not already scraped."""
        products = response_json.get("products", [])
        
        for product in products:
            product_id = str(product.get("productId"))
            product_url = product.get("url")
            
            # If the product has already been saved, skip it
            if product_id in self.scraped_data["products"]:
                continue

            self.scraped_data["products"][product_id] = {
                "url": product_url,
                "visited": False  # Mark as not yet visited for details
            }
        
        # Save current progress
        self.save_source_of_truth()

    def parse_product_page(self, response):
        """Extract detailed product information from individual product page."""
        product_id = response.meta["product_id"]
        product_info = self.scraped_data["products"][product_id]

        # Extract product name
        product_name = response.css('.product-name-class::text').get()
        if product_name:
            product_info["product_name"] = product_name.strip()

        # Extract major ingredients
        major_ingredients = response.css('.productDetailPage_accordionContent__tZh8X span::text').getall()
        if major_ingredients:
            product_info["major_ingredients"] = ', '.join([ingredient.strip() for ingredient in major_ingredients])

        # Mark this product as visited and update source of truth
        product_info["visited"] = True
        self.save_source_of_truth()

        # Append the updated product info to the final output JSON
        self.save_to_final_output(product_info)

    def save_to_final_output(self, product_info):
        """Save the final product data to the output JSON file."""
        if not self.output_file.exists():
            with open(self.output_file, "w", encoding="utf-8") as f:
                json.dump({"products": []}, f, indent=4)

        with open(self.output_file, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data["products"].append(product_info)
            f.seek(0)
            json.dump(data, f, indent=4)
