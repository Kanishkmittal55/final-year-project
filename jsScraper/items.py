# # Define here the models for your scraped items
# #
# # See documentation in:
# # https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ChemEntry(scrapy.Item):
    site_url = scrapy.Field()
    brand_name = scrapy.Field()
    product_name = scrapy.Field()
    product_type = scrapy.Field()
    claimed_ingredient_name = scrapy.Field()
    key_ingredients = scrapy.Field()
    price = scrapy.Field()


class ProductItem(scrapy.Item):
    product_id = scrapy.Field()
    name = scrapy.Field()
    images = scrapy.Field()
    brand_name = scrapy.Field()
    brand_id = scrapy.Field()
    sell_price = scrapy.Field()
    list_price = scrapy.Field()
    discount = scrapy.Field()
    discount_value = scrapy.Field()
    color_css = scrapy.Field()
    account_id = scrapy.Field()
    attribute_ids = scrapy.Field()
    show_yesties_badge_icon = scrapy.Field()
    url = scrapy.Field()
    ingredients = scrapy.Field()
    category = scrapy.Field()
