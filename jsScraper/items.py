# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ChemEntry(scrapy.Item):
    site_url = scrapy.Field()
    brand_name = scrapy.Field()
    product_name = scrapy.Field()
    product_type = scrapy.Field()
    claimed_ingredient_name = scrapy.Field()
    key_ingredients = scrapy.Field()
    price = scrapy.Field()
