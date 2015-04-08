# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KickassItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()

class warezbbItem(scrapy.Item):
    author = scrapy.Field()
    replies = scrapy.Field()
    views = scrapy.Field()
    post_date = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()


