import scrapy
import json
from jsScraper.items import ChemEntry  # Import the ChemEntry item

class TheordinarySpider(scrapy.Spider):
    name = "theordinary"
    start_urls = ["https://theordinary.com/en-gb/category/skincare"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }

    def __init__(self):
        self.debug_data = {
            'category_links': [],
            'product_links': [],
            'missing_ingredients': []
        }

    def start_requests(self):
        # Start with the provided URL
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_category)

    def parse_category(self, response):
        # Extract category links
        category_links = response.css('.refinement-group-body ul.list-group li a.filters_item::attr(href)').getall()

        # For now, limit to the first two category links
        # category_links = category_links[:2]
        # print(category_links)

        # Full URL construction
        base_url = "https://theordinary.com"
        full_urls = [base_url + link for link in category_links]

        # Log and save the extracted links
        self.log(f"Extracted {len(full_urls)} category links.")
        self.debug_data['category_links'] = full_urls  # Save to debug data

        # Write the debug data so far to the debug_output.json file
        self.write_debug_data()

        # Visit each category link
        for url in full_urls:
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_products, meta={'link': url})

    def parse_products(self, response):
        # Extract the product information from the page
        product_containers = response.css('.product-grid-item')

        for product in product_containers:
            # Extract product details
            title = product.css('.pdp-link a::text').get()
            price = product.css('.price .sales .value::text').get()
            targets = product.css('.concern .concern-value::text').get()
            suited_to = product.css('.suited-value::text').get()

            product_link = product.css('.pdp-link a::attr(href)').get()
            product_url = response.urljoin(product_link)

            # Log and save the individual product link
            self.log(f"Extracted product link: {product_url}")
            self.debug_data['product_links'].append(product_url)  # Save to debug data

            # Create a ChemEntry item
            item = ChemEntry(
                site_url=product_url,
                brand_name="The Ordinary",  # Since we are scraping The Ordinary products
                product_name=title if title else "NA",  # Using product title as the product type
                product_type=suited_to if suited_to else "NA",
                claimed_ingredient_name=targets if targets else "NA",  # Assuming 'targets' could refer to claimed ingredients
                price=price if price else "Not available"  # Use the extracted price
            )

            # Yield the item to the pipeline after following the product link for detailed information
            yield scrapy.Request(url=product_url, headers=self.headers, callback=self.parse_product_details, meta={'item': item, 'link': product_url})

    def parse_product_details(self, response):
        # Get the item passed from the previous method
        item = response.meta['item']

        # Extract ingredients from the ingredients section
        ingredients = response.css('.ingredients-flyout-content::text').get()

        if ingredients:
            # Clean up and strip any extra whitespace or newlines
            item['key_ingredients'] = ingredients.strip()
        else:
            # Log the missing ingredient and the targeted CSS for debugging
            item['key_ingredients'] = "NA"
            self.debug_data['missing_ingredients'].append({
                'product_url': response.meta['link'],
                'css_targeted': '.ingredients-flyout-content::text'
            })

        # Log the product details with ingredients for debugging
        self.log(f"Product details with ingredients: {item['key_ingredients']} for {item['product_type']}")

        # Write the debug data to the debug_output.json file after parsing product details
        self.write_debug_data()

        # Yield the updated item with ingredients
        yield item

    def write_debug_data(self):
        # Write debug data to a file
        with open("debug_output.json", "w", encoding='utf-8') as f:
            json.dump(self.debug_data, f, ensure_ascii=False, indent=4)
