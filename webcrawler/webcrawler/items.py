# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KickassItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    downloads = scrapy.Field()
    post_date = scrapy.Field()
    replies = scrapy.Field()

class WarezbbItem(scrapy.Item):
    catalog_id = scrapy.Field()
    author = scrapy.Field()
    replies = scrapy.Field()
    views = scrapy.Field()
    post_date = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()


