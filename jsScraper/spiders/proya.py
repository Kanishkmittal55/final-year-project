import scrapy
import re  # For cleaning up unwanted characters
from jsScraper.items import ChemEntry

class ProyaSpider(scrapy.Spider):
    name = "proya"
    start_urls = ["https://www.proya-group.com/en/component2"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    def parse(self, response):
        # Extracting the category list with hrefs
        categories = response.css('.c-list.font18 a')
        
        # Get the number of categories
        category_count = len(categories)
        self.log(f"\033[91m\033[1mProya has {category_count} categories\033[0m")  # Output in red and bold

        # Loop over each category and follow the link
        for category in categories:
            category_name = category.css('::text').get()
            category_link = category.css('::attr(href)').get()
            
            # Complete the relative link to form a full URL
            category_url = response.urljoin(category_link)
            
            # Send a request to parse the category page
            yield scrapy.Request(
                url=category_url,
                headers=self.headers,
                callback=self.parse_category,
                meta={'category_name': category_name}
            )

    def parse_category(self, response):
        category_name = response.meta['category_name']

        # Clean up the description text (removing \r\n and spaces)
        items = response.css('.c-list2-box .c-wrap')  # Loop through each product entry

        for item in items:
            product_title = item.css('.c-title.font24::text').get()
            
            # Extract the product description without images and clean it up
            description = item.css('.public-content').xpath("descendant-or-self::*/text()[not(ancestor::img)]").getall()
            description = ' '.join(description).strip()  # Join and clean up the text
            description = re.sub(r'\s+', ' ', description)  # Remove extra whitespace, newlines, etc.
            
            # Since Proya site may not provide ingredient data directly, setting placeholder values
            key_ingredients = "NA"  # Placeholder as no data provided
            claimed_ingredient_name = "NA"  # Placeholder as no data provided
            price = "Not available"  # Assuming no price data is provided

            # Create a ChemEntry item similar to Bloomage and Sephora
            item = ChemEntry(
                site_url=response.url,
                brand_name="Proya",  # Static as we are scraping from Proya
                product_type=product_title if product_title else "NA",
                claimed_ingredient_name=claimed_ingredient_name,
                key_ingredients=key_ingredients,
                price=price
            )

            # Yield the item to the pipeline
            yield item

        # Log the category and number of products processed
        self.log(f"Processed products for category {category_name}.")
