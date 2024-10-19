import scrapy
import json
from jsScraper.items import ChemEntry

class BloomageSpider(scrapy.Spider):
    name = "bloomage"
    page_index = 1  # Start with the first page
    total_pages = 7  # Assuming we have 7 pages
    api_url = "https://www.bloomagebioactive.com/API/Common/GetDataList?columnId=10127&pageIndex={}&pageSize=10&order=Sort%20desc&whereJson=%7B%7D"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    def start_requests(self):

        yield scrapy.Request(url=self.api_url.format(self.page_index), headers=self.headers, callback=self.parse)

    def parse(self, response):
        # Parse the JSON response
        data = json.loads(response.text)


        if data.get('success'):
            # Extract products from the response
            products = data.get('data', [])
            print(products)  # This will print the products to your console for debugging purposes

            # Create a structure for storing data
            page_data = {
                'Link': self.api_url.format(self.page_index),
                'Number of query': self.page_index,
                'Data': []
            }

            # Collect product data
            for product in products:
                # Create a ChemEntry item
                item = ChemEntry(
                    site_url=self.api_url.format(self.page_index),
                    brand_name=product.get('Title'),  # Assuming the brand is static for this site
                    product_type = 'NA',  # Assuming 'Title' contains product type
                    claimed_ingredient_name=product.get('SubTitle'),  # Assuming 'SubTitle' contains ingredients
                    key_ingredients= 'NA',  # You may split this if it's a list
                    price="Not available"  # Assuming no price data is available from the API
                )
                
                yield item
            # Move to the next page if there are more pages
            if self.page_index < self.total_pages:
                self.page_index += 1
                yield scrapy.Request(url=self.api_url.format(self.page_index), headers=self.headers, callback=self.parse)
            else:
                self.log("All pages processed successfully.")
        else:
            self.log("Failed to retrieve data from the API.")
