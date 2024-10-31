import scrapy
from playwright_stealth import stealth_sync

class YesStyleSpider(scrapy.Spider):
    name = "yesstyle"

    start_urls = [
        "https://www.yesstyle.com/en/beauty-lips/list.html/bcc.15495_bpt.46"
    ]

    custom_settings = {
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": False,  # Set to False if you want to see the browser in action
        },
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers=self.headers,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                },
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        stealth_sync(page)  # Apply stealth mode

        # Create the output file and start writing
        file_path = "yesstyle_products.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("YesStyle Products:\n\n")

        current_page = 1
        max_scrolls = 30  # Adjust if you want more or fewer pages

        for _ in range(max_scrolls):
            self.log(f"Scraping page {current_page}")
            
            # Scroll to the bottom to trigger loading more products
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            await page.wait_for_timeout(5000)  # Adjust delay if needed

            # Capture any new API response triggered by the scroll
            async with page.expect_response(lambda r: "rest/products/v1/department" in r.url) as resp_info:
                response_api = await resp_info.value
                response_json = await response_api.json()

                # Write the extracted data from JSON to the file
                self.parse_products(response_json, current_page, file_path)

            current_page += 1

        await page.close()

    def parse_products(self, response_json, current_page, file_path):
        """Extracts product data from the JSON API response and appends it to a file"""
        products = response_json.get("products", [])

        if not products:
            self.log(f"No products found on page {current_page}")
            return

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"\n\nPAGE {current_page}\n\n")
            for product in products:
                # Write all key-value pairs for each product
                for key, value in product.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n")  # Separate each product with a newline

        self.log(f"Page {current_page} products appended to {file_path}")
