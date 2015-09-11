import scrapy
import sys
import re

class warezbb_thread_link_collector_spider(scrapy.Spider):
    name = "warezLink"
    allowed_domains = ["https://www.warez-bb.org/*"]
    download_delay = 6
    start_urls = ["https://www.warez-bb.org/login.php"]
    sticked_titles_id = [
        "21537617",
        "21451815",
        "21626981",
        "15678",
        "21399630",
        "6000413",
        "4170791",
        "2538913",
        "2538871",
        "589688",
        "16040260",
        "589689",
        "21793204"
    ]
    curr_page = 0
    start_page = 0
    end_page = 100000
    movie_forum_page = "https://www.warez-bb.org/viewforum.php?f=4"

    def parse(self, response):
        """ Makes request to login onto warezbb
            with after_login as a callback
        """
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'nzgangster', 'password': 'KANyezus'},
            callback=self.after_login, dont_filter=True
        )

    def after_login(self, response):
        """ Checks that the spider has logged on
            and makes a number of requests to
            warez-bb sub-forums.
        """
        if "authentication failed" in response.body:
            print "Failed to Log in, exiting now"
            return
        else:
            yield scrapy.Request(url=self.movie_forum_page,
                meta={'id': self.catalog_id["movie"]},
                callback=self.parse_outside_post, dont_filter=True)

    def parse_outside_post(self, response):
        if self.curr_page > self.end_page:
           # raise CloseSpider("crawled " + str(self.end_page))
           pass
        else:
            if self.curr_page >= self.start_page:
                f = open("numberOfPagesWarezMovies2.txt","w")
                f.write(str(self.curr_page))
                rows = response.xpath("//div[@class='list-rows']")
                for row in rows:
                    replies = row.xpath(".//div[@class='topics']/span/text()")
                    replies = replies.extract()
                    replies = replies[0]

                    views = row.xpath(".//div[@class='views']/span/text()")
                    views = views.extract()
                    views = views[0]

                    link = row.xpath(".//div/span/span[@class='title']/a/@href")
                    link = link.extract()
                    link_string = str(link)
                    link_id = link_string[link_string.index("=")+1:]
                    if link_id[:-2] not in self.sticked_titles_id:
                        link = "https://www.warez-bb.org/" + link[0]
                        f = open("linksWarezbb3.txt", "a")
                        f.write((str(link)) + " " + str(replies) + " " + str(views) +"\n")
            try:
                self.curr_page = self.curr_page + 1
                current_page = response.xpath("//b[@class='active-button']")
                current_page = current_page[0].xpath('text()').extract()[0]
                next_page = int(current_page) + 1
                next_link = response.xpath("//a[@title='Page " + str(next_page) + "']/@href")
                next_link = "https://www.warez-bb.org/" + next_link[0].extract()
                yield scrapy.Request(url=next_link,
                    callback=self.parse_outside_post, dont_filter=True)
            except Exception as e:
                print type(e)
                print e.args
                print e
                pass
