# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def fix_name(value):
    return value[5:-3]


class ProfileItem(scrapy.Item):
    person = scrapy.Field()
