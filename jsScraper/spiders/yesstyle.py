import scrapy
from playwright_stealth import stealth_sync
from jsScraper.items import ProductItem  # Adjust "myproject" to the name of your Scrapy project
import asyncio
import re

class YesStyleSpider(scrapy.Spider):
    name = "yesstyle"

    start_urls = [
        # "https://www.yesstyle.com/en/beauty-cheeks/list.html/bcc.15500_bpt.46",
        # "https://www.yesstyle.com/en/beauty-eyes/list.html/bcc.15488_bpt.46",
        # "https://www.yesstyle.com/en/beauty-face/list.html/bcc.15480_bpt.46",
        # "https://www.yesstyle.com/en/beauty-lips/list.html/bcc.15495_bpt.46",

        # "https://www.yesstyle.com/en/beauty-bath-shower/list.html/bcc.15573_bpt.46",
        # "https://www.yesstyle.com/en/beauty-body-moisturizers/list.html/bcc.15578_bpt.46",
        # "https://www.yesstyle.com/en/beauty-deodorants/list.html/bcc.15582_bpt.46", ( Handle cases has only 2 pages of items )
        # "https://www.yesstyle.com/en/beauty-foot-care/list.html/bcc.15581_bpt.46", ( Had only 4 pages )

        # "https://www.yesstyle.com/en/beauty-hair-treatments/list.html/bcc.15592_bpt.46",
        # "https://www.yesstyle.com/en/beauty-shampoos/list.html/bcc.15587_bpt.46",

        # "https://www.yesstyle.com/en/beauty-face-cleansers/list.html/bcc.15545_bpt.46",
        # "https://www.yesstyle.com/en/beauty-face-serums/list.html/bcc.15556_bpt.46",
        # "https://www.yesstyle.com/en/beauty-moisturizers/list.html/bcc.15569_bpt.46", ( I think the item is not being yield in this page different config why ?)
        # "https://www.yesstyle.com/en/beauty-toners/list.html/bcc.15552_bpt.46", ( Same as above )

        # "https://www.yesstyle.com/en/beauty-sunscreens/list.html/bcc.15601_bpt.46",  ( Same as above )
        # "https://www.yesstyle.com/en/beauty-after-sun-care/list.html/bcc.15602_bpt.46", ( " ) 
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
        "CONCURRENT_REQUESTS": 1,  # Set to 1 to ensure requests are handled one by one
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "AUTOTHROTTLE_ENABLED": True,
        "DOWNLOAD_DELAY": 2,  # Adds a delay of 2 seconds between requests to avoid hitting rate limits
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    # Extract category from the start_url
    def parse_category_from_url(self, url):
        match = re.search(r"/en/([^/]+)/list", url)
        return match.group(1) if match else "unknown-category"

    def start_requests(self):
        for url in self.start_urls:
            # Extract category from each URL
            category = self.parse_category_from_url(url)

            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers=self.headers,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "category": category,  # Pass the category as metadata
                },
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        stealth_sync(page)  # Apply stealth mode

        current_page = 1
        max_scrolls = 5  # Adjust if you want more or fewer pages

        for _ in range(max_scrolls):
            self.log(f"Scraping page {current_page} for category {response.meta['category']}")
            
            async with page.expect_response(lambda r: "rest/products/v1/department" in r.url, timeout=10000) as resp_info:
                await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                await page.wait_for_timeout(5000)

                response_api = await resp_info.value
                response_json = await response_api.json()

                async for item in self.parse_products(response_json, response.meta["category"], current_page):
                    yield item

            current_page += 1

        await page.close()

    async def parse_products(self, response_json, category, current_page):
        products = response_json.get("products", [])

        if not products:
            self.log(f"No products found on page {current_page} for category {category}")
            return

        for entry in products:
            product = entry.get("product", {})

            item = ProductItem()
            item['product_id'] = product.get("productId")
            item['name'] = product.get("name")
            item['images'] = product.get("images", {}).get("m")
            item['brand_name'] = product.get("brandName")
            item['brand_id'] = product.get("brandId")

            sell_price_raw = product.get("sellPrice", "")
            list_price_raw = product.get("listPrice", "")

            item['sell_price'] = sell_price_raw.replace("&pound;", "").replace("&nbsp;", "").strip()
            item['list_price'] = list_price_raw.replace("&pound;", "").replace("&nbsp;", "").strip()

            item['discount'] = product.get("discount")
            item['discount_value'] = product.get("discountValue")
            item['color_css'] = product.get("colorCss")
            item['account_id'] = product.get("accountId")
            item['attribute_ids'] = product.get("attributeIds")
            item['show_yesties_badge_icon'] = product.get("showYestiesBadgeIcon")
            item['url'] = entry.get("url")

            # Assign the category dynamically from response.meta
            item['category'] = category

            yield item
