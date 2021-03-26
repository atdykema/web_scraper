# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def fix_name(value):
    return value[5:-3]


class ProfileItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(fix_name),
                        output_processor=TakeFirst())
    location = scrapy.Field()
    date_of_incident = scrapy.Field()
    crime = scrapy.Field()
    sex = scrapy.Field()
    height = scrapy.Field()
    build = scrapy.Field()
    hair_color = scrapy.Field()
    hair_length = scrapy.Field()
    ethic_appearance = scrapy.Field()
    additional_info = scrapy.Field()