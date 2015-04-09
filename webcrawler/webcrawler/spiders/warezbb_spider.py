
import scrapy
from webcrawler.items import WarezbbItem
#KANyezus

class WarezbbSpider(scrapy.Spider):
    name = "warezbb"
    allowed_domains = ["https://www.warez-bb.org/"]

    start_urls = [
       "https://www.warez-bb.org/login.php"
    ]

    forum_links = {
    "movies": "https://www.warez-bb.org/viewforum.php?f=4",
    "games" : "https://www.warez-bb.org/viewforum.php?f=5",
    "apps"  : "https://www.warez-bb.org/viewforum.php?f=3",
    "music" : "https://www.warez-bb.org/viewforum.php?f=6"
    }

    catalog_ids = {
    "movies": "0",
    "apps"  : "1",
    "music" : "2",
    "games" : "3",
    "tv"    : "4"
    }

    # keeps track of how many pages each sub forum
    # was parsed
    INeedABetterName = {
    "0": 0,
    "1" : 0,
    "2"  : 0,
    "3" : 0,
    "4" : 0
    }

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'nzgangster', 'password': 'KANyezus'},
            callback=self.after_login, dont_filter=True
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            print "Failed to Log in, exiting now"
            return
        else:
            print "Logged in"
            for key in self.forum_links:
                yield scrapy.Request(url=self.forum_links[key],
                    callback=self.parse_items, dont_filter=True)


    def parse_items(self, response):
        link_title = response.xpath("//title/text()").extract()
        catalog_id = self.get_catalog_id(link_title[0])
        
        # checks how many pages parsed, if more than 25
        # exit. 
        if self.INeedABetterName[catalog_id] > 25:
            return

        # get all list rows
        # for each row, if it starts with a [ following the [RG...] format
        # get info
        # else
        # ignore

        rows = response.xpath("//div[@class='list-rows']")
        for row in rows:
            item = WarezbbItem()
            title = row.xpath(".//div/span/span[@class='title']/a/text()")
            title = title.extract()[0].strip()
            if title[0] == "[":
                
                author = row.xpath(".//div[@class='posts']/span/a/text()").extract()
                replies = row.xpath(".//div[@class='topics']/span/text()").extract()
                views = row.xpath(".//div[@class='views']/span/text()").extract()
                post_date = row.xpath(".//div[@class='last-post']/span/a/text()").extract()
                link = row.xpath(".//div/span/span[@class='title']/a/@href").extract()

                item["catalog_id"] = catalog_id
                item["author"] = author
                item["replies"] = replies
                item["views"] = views
                item["post_date"] = post_date
                item["title"] = title
                item["link"] = link

                yield item

        self.INeedABetterName[catalog_id] = self.INeedABetterName[catalog_id] + 1

        current_page = response.xpath("//b[@class='active-button']")
        current_page = current_page[0].xpath('text()').extract()[0]
        next_page = int(current_page) + 1
        next_link = response.xpath("//a[@title='Page " + str(next_page) + "']/@href")
        next_link = "https://www.warez-bb.org/" + next_link[0].extract()

        yield scrapy.Request(url=next_link,
            callback=self.parse_items, dont_filter=True)

    def get_catalog_id(self, string):
        for key in self.catalog_ids:
            if key in string.lower():
                return self.catalog_ids[key]
