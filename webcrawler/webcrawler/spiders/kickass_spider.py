import scrapy
from webcrawler.items import KickassItem

class kickassSpider(scrapy.Spider):
    name = "kickass"
    allowed_domains = ["kickass.to"]
    start_urls = [
       "https://kickass.to/movies/"
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@class="markeredBlock torType filmType"]'):
            item = KickassItem()

            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()

            yield item

