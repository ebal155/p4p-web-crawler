import scrapy
from webcrawler.items import WarezbbItem


class WarezbbSpider(scrapy.Spider):
    """ This class is a spider which crawls the warezbb subforum and gets
        data from 4 subforums. 
    """
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
    # have been parsed
    pages_parsed = {
    "0": 0,
    "1" : 0,
    "2"  : 0,
    "3" : 0,
    "4" : 0
    }

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
            print "Logged in"
            for key in self.forum_links:
                yield scrapy.Request(url=self.forum_links[key],
                    callback=self.parse_items, dont_filter=True)



    def parse_items(self, response):
        """ Parses the current page and gets relevant info.     
            Will also make a request to next page if there is 
            a next page and the spider hasn't gone over the limit
        """
        link_title = response.xpath("//title/text()").extract()
        catalog_id = self.get_catalog_id(link_title[0])
    
        # checks how many pages parsed for current subforum
        # if more than 25 exit.
        if self.pages_parsed[catalog_id] > 25:
            print self.pages_parsed
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

                author = row.xpath(".//div[@class='posts']/span/a/text()")
                author = author.extract()
                author = author[0]

                replies = row.xpath(".//div[@class='topics']/span/text()")
                replies = replies.extract()
                replies = replies[0]

                views = row.xpath(".//div[@class='views']/span/text()")
                views = views.extract()
                views = views[0]

                post_date = row.xpath(".//div[@class='last-post']/span/a/text()")
                post_date = post_date.extract()
                post_date = post_date[0]

                link = row.xpath(".//div/span/span[@class='title']/a/@href")
                link = link.extract()
                link = "https://www.warez-bb.org/" + link[0]

                item["catalog_id"] = catalog_id
                item["author"] = author
                item["replies"] = replies
                item["views"] = views
                item["post_date"] = post_date
                item["title"] = title
                item["link"] = link

                yield item

        self.pages_parsed[catalog_id] = self.pages_parsed[catalog_id] + 1

        current_page = response.xpath("//b[@class='active-button']")
        current_page = current_page[0].xpath('text()').extract()[0]
        next_page = int(current_page) + 1
        next_link = response.xpath("//a[@title='Page " + str(next_page) + "']/@href")
        next_link = "https://www.warez-bb.org/" + next_link[0].extract()

        yield scrapy.Request(url=next_link,
            callback=self.parse_items, dont_filter=True)

    def get_catalog_id(self, string):
        """ Gets the correct id for each item type """
        for key in self.catalog_ids:
            if key in string.lower():
                return self.catalog_ids[key]
