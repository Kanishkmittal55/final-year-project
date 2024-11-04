import scrapy
from playwright_stealth import stealth_sync
from jsScraper.items import ProductItem  # Adjust "myproject" to the name of your Scrapy project
import asyncio

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

        # Add an event listener to log all network requests made by the page
        page.on("response", lambda response: self.logger.info(f"Network request: {response.url} - Status: {response.status}"))

        current_page = 1
        max_scrolls = 2  # Adjust if you want more or fewer pages

        for _ in range(max_scrolls):
            self.log(f"Scraping page {current_page}")
            
            # Start listening for the response first
            async with page.expect_response(lambda r: "rest/products/v1/department" in r.url, timeout=10000) as resp_info:
                # Scroll to the bottom to trigger loading more products
                await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                await page.wait_for_timeout(5000)  # Adjust delay if needed

                # Capture the response after scrolling
                response_api = await resp_info.value
                response_json = await response_api.json()

                # Process the response
                async for item in self.parse_products(response_json, current_page):
                    yield item

            current_page += 1

        await page.close()

    async def parse_products(self, response_json, current_page):
        """Extracts product data from the JSON API response and yields ProductItem instances asynchronously."""
        # Extract the list of products from the response JSON
        products = response_json.get("products", [])

        if not products:
            self.log(f"No products found on page {current_page}")
            return

        for entry in products:
            # Access the nested "product" dictionary inside each entry
            product = entry.get("product", {})

            # Create a new ProductItem and map fields correctly based on the JSON structure
            item = ProductItem()
            item['product_id'] = product.get("productId")  # Access "productId" inside the nested "product" dictionary
            item['name'] = product.get("name")
            item['images'] = product.get("images", {}).get("m")  # Fetches the medium image URL if available
            item['brand_name'] = product.get("brandName")
            item['brand_id'] = product.get("brandId")
            item['sell_price'] = product.get("sellPrice")
            item['list_price'] = product.get("listPrice")
            item['discount'] = product.get("discount")
            item['discount_value'] = product.get("discountValue")
            item['color_css'] = product.get("colorCss")
            item['account_id'] = product.get("accountId")
            item['attribute_ids'] = product.get("attributeIds")
            item['show_yesties_badge_icon'] = product.get("showYestiesBadgeIcon")
            item['url'] = entry.get("url")

            # Use async yield to make this function an async generator
            yield item


