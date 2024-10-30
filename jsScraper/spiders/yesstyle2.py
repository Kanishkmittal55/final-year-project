import scrapy

class Yesstyle2Spider(scrapy.Spider):
    name = "yesstyle2"

    custom_settings = {
        'DOWNLOAD_DELAY': 10,  # Delay of 1 second between requests
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  # Max 5 requests per domain at once
        'AUTOTHROTTLE_ENABLED': True,  # Enable AutoThrottle to dynamically adjust delays
        'AUTOTHROTTLE_START_DELAY': 1,  # The initial delay before making requests
        'AUTOTHROTTLE_MAX_DELAY': 5,  # The maximum delay to throttle
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,  # Average number of requests Scrapy should be sending
        'AUTOTHROTTLE_DEBUG': False,  # Disable showing throttling stats
        'USER_AGENT': 'Mozilla/5.0',  # Fallback User-Agent
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        }
    }

    def read_urls_from_file(self, file_path):
        with open(file_path, "r") as file:
           urls = [line.strip() for line in file if line.strip()]
        return urls 

    def start_requests(self):
        file_path = "extracted_products.txt"
        urls = self.read_urls_from_file(file_path)

        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_product_page
            )

    def parse_product_page(self, response):
        # Create a dictionary to store the product details
        product_info = {}

        # Example: Extract the product name (optional, adjust selector as per site structure)
        product_name = response.css('.product-name-class::text').get()  # Replace with the actual class if needed
        if product_name:
            product_info['product_name'] = product_name.strip()

        # Extract Major Ingredients
        major_ingredients = response.css('.productDetailPage_accordionContent__tZh8X span::text').getall()
        if major_ingredients:
            product_info['major_ingredients'] = ', '.join([ingredient.strip() for ingredient in major_ingredients])

        # Log the extracted information
        self.log(f"Extracted product info: {product_info}")

        # Optionally write the extracted info to a file
        file_path = "yesstyle_product_details.txt"
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"Product URL: {response.url}\n")
            f.write(f"Product Name: {product_info.get('product_name', 'N/A')}\n")
            f.write(f"Major Ingredients: {product_info.get('major_ingredients', 'N/A')}\n")
            f.write("\n" + "=" * 50 + "\n")  # Separator between products
