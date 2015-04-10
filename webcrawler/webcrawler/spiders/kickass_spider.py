
import scrapy
from webcrawler.items import KickassItem
#KANyezus

class WarezbbSpider(scrapy.Spider):
    name = "kickass"
    allowed_domains = ["https://kickass.to/"]

    start_urls = [
       "https://kickass.to"
    ]

    #Make request to a number of pages of movies with parse_movie_page as a callback
    def parse(self, response):
        num_pages = 11

        for x in range(0,11):
            if (x == 0):
                yield scrapy.Request(url="https://kickass.to/movies/",callback=self.parse_movie_page,dont_filter=True)
            else:
                yield scrapy.Request(url="https://kickass.to/movies/" + str(x) + "/",callback=self.parse_movie_page,dont_filter=True)

    #Parse and make a request to each movie link inside a movie page with parse_movie as a callback
    def parse_movie_page(self,response):
        list_movies_url = response.xpath(".//div[@class='markeredBlock torType filmType']/a/@href").extract()

        for url in list_movies_url:
            movie_page = "https://kickass.to" + url
            yield scrapy.Request(url=movie_page,callback=self.parse_movie,dont_filter=True)
    
    #Make a request to a movie page, and parse the relevant information
    def parse_movie(self,response):
        item = KickassItem()

        title = response.xpath(".//h1[@class='novertmarg']/a/span/text()").extract()
        title[0]

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