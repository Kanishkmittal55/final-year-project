from playwright_stealth import stealth
import scrapy

class YesStyleSpider(scrapy.Spider):
    name = "yesstyle"

    # Start URLs for the category we want to scrape
    start_urls = [
        "https://www.yesstyle.com/en/beauty-cheeks/list.html/bcc.15500_bpt.46"
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

        # Apply stealth mode to Playwright to avoid bot detection
        await stealth(page)

        # Wait for 5 seconds
        await page.wait_for_timeout(10000)

        # Close the Playwright page
        await page.close()

        self.log("Playwright page has been closed after 5 seconds.")
