import scrapy
import sys
from webcrawler.items import warezbbItem
#KANyezus

class warezbbSpider(scrapy.Spider):
    name = "warezbb"
    allowed_domains = ["https://www.warez-bb.org/"]
    start_urls = [
       "https://www.warez-bb.org/login.php"
    ]
    forum_links = {
    "movies": "https://www.warez-bb.org/viewforum.php?f=4"
    }

    pages_parsed = 0

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'nzgangster', 'password': 'KANyezus'},
            callback=self.after_login, dont_filter=True
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.log("Login failed", level=log.ERROR)
            return
        else:
            print "Logged in"
            yield scrapy.Request(url=self.forum_links["movies"], callback=self.parse_movies, dont_filter=True)

    def parse_movies(self, response):
        """This method goes through the sub forum movies and gets the link on the page"""

        if self.pages_parsed > 25:
            sys.exit("25 pages_parsed");
        # get all list rows
        # for each row, if it starts with a [ following the [RG...] format, go inside
        # else ignore
        rows = response.xpath("//div[@class='list-rows']")
        for row in rows:
            item = warezbbItem()
            title = row.xpath(".//div/span/span[@class='title']/a/text()").extract()[0].strip()
            if title[0] == "[":
                author = row.xpath(".//div[@class='posts']/span/a/text()").extract()
                replies = row.xpath(".//div[@class='topics']/span/text()").extract()
                views = row.xpath(".//div[@class='views']/span/text()").extract()
                post_date = row.xpath(".//div[@class='last-post']/span/a/text()").extract()
                link = row.xpath(".//div/span/span[@class='title']/a/@href").extract()
                item["author"] = author
                item["replies"] = replies
                item["views"] = views
                item["post_date"] = post_date
                item["title"] = title
                item["link"] = link
                yield item
        self.pages_parsed = self.pages_parsed + 1
        current_page = response.xpath("//b[@class='active-button']")
        current_page = current_page[0].xpath('text()').extract()[0]
        next_page = int(current_page) + 1
        next_link = response.xpath("//a[@title='Page " + str(next_page) + "']/@href")
        next_link = "https://www.warez-bb.org/" + next_link[0].extract()
        yield scrapy.Request(url=next_link, callback=self.parse_movies, dont_filter=True)