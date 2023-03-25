import scrapy


class PropertyItem(scrapy.Item):
    id = scrapy.Field()
    front_img = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    link = scrapy.Field()
    property_type = scrapy.Field()
