import scrapy
import psycopg2

class Yesstyle2Spider(scrapy.Spider):
    name = "yesstyle2"

    custom_settings = {
        'DOWNLOAD_DELAY': 8,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 5,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
        'USER_AGENT': 'Mozilla/5.0',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        }
    }

    def __init__(self, *args, **kwargs):
        super(Yesstyle2Spider, self).__init__(*args, **kwargs)
        # Database connection
        self.connection = psycopg2.connect(
            host="dpg-csiveslsvqrc73ekljr0-a.oregon-postgres.render.com",
            database="scraper_e6jv",
            user="scraper_e6jv_user",
            password="KYecsGcmpFath3iCkpolng4y8XGvZ3rE",
            port="5432"
        )
        self.cursor = self.connection.cursor()

    def start_requests(self):
        # Fetch all product URLs from the database
        table_name = "products"
        self.cursor.execute(f"SELECT url FROM {table_name} WHERE ingredients IS NULL OR ingredients = ''")
        urls = self.cursor.fetchall()

        # Yield a request for each URL
        for url_tuple in urls:
            url = url_tuple[0]
            yield scrapy.Request(url=url, callback=self.parse_product_page, errback=self.handle_error)

    def parse_product_page(self, response):
        # Extract major ingredients
        major_ingredients = response.css('.productDetailPage_accordionContent__tZh8X span::text').getall()
        if major_ingredients:
            ingredients = ', '.join([ingredient.strip() for ingredient in major_ingredients])
        else:
            ingredients = None  # Leave as NULL if not found

        # Update the database with the ingredients
        table_name = "products"
        self.cursor.execute(
            f"UPDATE {table_name} SET ingredients = %s WHERE url = %s",
            (ingredients, response.url)
        )
        self.connection.commit()

        self.log(f"Updated ingredients for {response.url}")

    def handle_error(self, failure):
        # Log the error without updating the `ingredients` field to any value
        self.logger.error(f"Failed to fetch ingredients for URL: {failure.request.url}")
        
        table_name = "products"
        self.cursor.execute(
            f"UPDATE {table_name} SET ingredients = NULL WHERE url = %s",
            (failure.request.url,)
        )
        self.connection.commit()

    def close(self, reason):
        # Close the database connection when spider closes
        self.cursor.close()
        self.connection.close()
