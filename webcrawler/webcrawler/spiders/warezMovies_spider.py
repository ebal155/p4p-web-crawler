import scrapy
import sys
from webcrawler.items import WarezbbItem


class WarezbbSpider(scrapy.Spider):
    name = "warezMovies"
    allowed_domains = ["https://www.warez-bb.org/"]

    download_delay = 5

    start_urls = [
       "https://www.warez-bb.org/login.php"
    ]

    forumPage = "https://www.warez-bb.org/viewforum.php?f=4"
    numberOfPages = 0
    catalog_id = 0

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
            yield scrapy.Request(url=self.forumPage,
                callback=self.parse_outside_post, dont_filter=True)


    def parse_outside_post(self, response):
        print "outside a post " + str(self.numberOfPages) 
        if self.numberOfPages > 1000:
            sys.exit()
        else:

            self.numberOfPages = self.numberOfPages + 1
            rows = response.xpath("//div[@class='list-rows']")
            for row in rows:
                item = WarezbbItem()

                title = row.xpath(".//div/span/span[@class='title']/a/text()")
                title = title.extract()[0].strip()

                item['title'] = title

                replies = row.xpath(".//div[@class='topics']/span/text()")
                replies = replies.extract()
                item['replies'] = replies[0]

                views = row.xpath(".//div[@class='views']/span/text()")
                views = views.extract()
                item['views'] = views[0]

                item['catalog_id'] = 0

                link = row.xpath(".//div/span/span[@class='title']/a/@href")
                link = link.extract()
                link = "https://www.warez-bb.org/" + link[0]
                item['link'] = link
                yield scrapy.Request(url=link,
                    meta={'item': item},
                    callback=self.parse_inside_post, dont_filter=True)

            current_page = response.xpath("//b[@class='active-button']")
            current_page = current_page[0].xpath('text()').extract()[0]
            next_page = int(current_page) + 1
            next_link = response.xpath("//a[@title='Page " + str(next_page) + "']/@href")
            next_link = "https://www.warez-bb.org/" + next_link[0].extract()

            yield scrapy.Request(url=next_link,
                callback=self.parse_outside_post, dont_filter=True)


    def parse_inside_post(self, response):
        item = response.meta['item']
        #//*[@id="84577963"]/div[1]/div/div[1]/strong

        author = response.xpath(".//div[@class='author']/strong")
        author = author.extract()
       
        try:
            author = author[0]
        except Exception:
            f1 = open('./testfile', 'a')
            f1.write("\n" + str(response.body))
            return
        item['author'] = author

        post_date = response.xpath(".//div[@class='date']/a/text()").extract()
        post_date = post_date[0]
        item['post_date'] = post_date

        yield item
