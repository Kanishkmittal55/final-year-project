import scrapy
import json
from scrapy.selector import Selector
from jsScraper.items import ChemEntry

class SephoraSpider(scrapy.Spider):
    name = "sephora"
    start_urls = ["https://www.sephora.com/buy/best-foundation-for-beginners"]
    sitemap_url = "https://www.sephora.com/sitemaps/buy-sitemap.xml"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }

    def start_requests(self):
        # First, yield a request to the sitemap
        yield scrapy.Request(url=self.sitemap_url, headers=self.headers, callback=self.parse_sitemap)

    def parse_sitemap(self, response):
        # Define the namespaces used in the XML
        ns = {
            'default': 'http://www.sitemaps.org/schemas/sitemap/0.9',
            'xhtml': 'http://www.w3.org/1999/xhtml'
        }
        
        # Parse the sitemap XML to extract URLs
        selector = Selector(response)
        sitemap_urls = selector.xpath('//default:url/default:loc/text()', namespaces=ns).getall()

        # Limit to the first 10 URLs for scraping
        first_10_urls = sitemap_urls[:10]

        # Log the number of URLs extracted from the sitemap
        self.log(f"Extracted {len(first_10_urls)} URLs for scraping.")

        # Send a request to each of the first 10 URLs
        for idx, url in enumerate(first_10_urls, start=1):
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_product_page, meta={'index': idx, 'url': url})

    def parse_product_page(self, response):
        # Extract meta information passed from the previous function
        index = response.meta['index']
        url = response.meta['url']

        # Iterate through product containers (modify the CSS selector if needed)
        product_elements = response.css('.css-1wtwtvo.eanm77i0')  # Example class for product containers

        for product in product_elements:
            # Extract product details
            product_name = product.css('h3 span.ProductName::text').get()
            brand_name = product.css('h3 span.css-1hs80e::text').get()
            price = product.css('p.css-1615o0y.eanm77i0::text').get()
            claimed_ingredient_name = product.css('p.css-1rsoa6d.eanm77i0::text').get()  # Assuming this field can map to ingredients

            # Additional information: Ingredient Callouts (could be key ingredients)
            key_ingredients = product.css('p.css-1hpjzzr::text').getall()
            key_ingredients = ', '.join(key_ingredients) if key_ingredients else 'NA'

            # Create a ChemEntry item similar to Bloomage
            item = ChemEntry(
                site_url=response.url,
                brand_name=brand_name if brand_name else "NA",
                product_type=product_name if product_name else "NA",
                claimed_ingredient_name=claimed_ingredient_name if claimed_ingredient_name else "NA",
                key_ingredients=key_ingredients,
                price=price if price else "Not available"
            )

            # Yield the item to the pipeline
            yield item

        # Log the extracted product details
        self.log(f"Extracted products from {url} (Link {index}).")
