# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KickassItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    author_reputation = scrapy.Field()
    downloads = scrapy.Field()
    post_date = scrapy.Field()
    replies = scrapy.Field()
    likes = scrapy.Field()
    dislikes = scrapy.Field()
    seeders = scrapy.Field()
    leechers = scrapy.Field()
    imdb_rating = scrapy.Field()
    rotten_tomatoes = scrapy.Field()
    detected_quality = scrapy.Field()
    movie_release_date = scrapy.Field()
    language = scrapy.Field()
    genre = scrapy.Field()
    file_size = scrapy.Field()
    cast = scrapy.Field()

class WarezbbItem(scrapy.Item):
    catalog_id = scrapy.Field()
    author = scrapy.Field()
    replies = scrapy.Field()
    views = scrapy.Field()
    post_date = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()



