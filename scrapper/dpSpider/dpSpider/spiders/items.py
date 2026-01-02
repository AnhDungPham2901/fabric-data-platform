import scrapy

class DemoItem(scrapy.Item):
    item_name = scrapy.Field()
    item_url = scrapy.Field()
    item_price = scrapy.Field()
    item_category = scrapy.Field()
    item_status = scrapy.Field()