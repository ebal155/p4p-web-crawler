
import scrapy
from webcrawler.items import KickassItem
#KANyezus

class WarezbbSpider(scrapy.Spider):
    name = "kickass"
    allowed_domains = ["https://kickass.to/"]

    start_urls = [
       "https://kickass.to/fast-and-furious-7-2015-hd-ts-xvid-ac3-hq-hive-cm8-t10472303.html"
    ]

    def parse(self, response):
        item = KickassItem()
        sel = response.body

        title = response.xpath(".//div[@class='torrentMediaInfo']/div/ul/li/a/span/text()").extract()
        title = title[0]

        author = response.xpath(".//div[@class='font11px lightgrey line160perc']/span/span/a/text()").extract()
        author = author[0]

        downloads = response.xpath(".//div[@class='font11px lightgrey line160perc']/text()").extract()
        downloads = downloads[3].split("Downloaded")[1].split("times")[0].strip()

        post_date = response.xpath(".//div[@class='font11px lightgrey line160perc']/text()").extract()
        post_date = post_date[0].split("Added on")[1].split("by")[0].strip()

        replies = response.xpath(".//div[@class='tabs tabSwitcher']/ul[@class='tabNavigation']/li/a/span/i/text()").extract()
        replies = replies[0]

        item["title"] = title
        item["author"] = author
        item["downloads"] = downloads
        item["post_date"] = post_date
        item["replies"] = replies

        yield item