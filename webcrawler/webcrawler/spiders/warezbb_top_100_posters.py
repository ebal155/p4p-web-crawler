import scrapy
from webcrawler.items import WarezbbAuthorItem

class Warezbb_top_100_posters_Spider(scrapy.Spider):
    name = "top_100"
    download_delay = 6
    start_urls = [
    "https://www.warez-bb.org/login.php"
    ]
    member_list_page_1 = "https://www.warez-bb.org/memberlist.php?mode=topten&g=&start=0"
    member_list_page_2 = "https://www.warez-bb.org/memberlist.php?mode=topten&g=&sid=9006051debc53cbd0c014f2410076c1e&start=50"

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
            yield scrapy.Request(url=self.member_list_page_1,
                callback=self.parse_outside_post, dont_filter=True)

    def parse_outside_post(self, response):
        """ goes through member list getting info"""
        # get the list_rows div, contains all members on this page
        rows = response.xpath('//div[@class="list-rows"]') 



        for row in rows.xpath('div'):
            item = WarezbbAuthorItem()
            divs = row.xpath('div')
            username = divs[1].xpath('span/strong/a/text()').extract()
            link = divs[1].xpath('span/strong/a/@href').extract()
            link = 'https://www.warez-bb.org/' + link[0]
            location = divs[3].xpath('span/text()').extract()
            join_date = divs[4].xpath('span/text()').extract()
            post_count = divs[5].xpath('span/a/text()').extract()
            item['username'] = username[0]
            item['link'] = link
            item['location'] = location[0].encode('utf8')
            item['join_date'] = join_date[0]
            item['post_count'] = post_count[0]
            yield scrapy.Request(url=link, meta={'item': item},
                 callback=self.parse_inside_post, dont_filter=True)
        yield scrapy.Request(url=self.member_list_page_2,
                callback=self.parse_outside_post, dont_filter=True)

    def parse_inside_post(self, response):
        """get remaining user info"""
        item = response.meta['item']
        user_info = response.xpath('.//div[@class="user-info"]')
        main_row = user_info.xpath('div[@class="main-rows"]')
        rows = main_row.xpath('div')
        post_information = rows[1].xpath('div/span/span[@class="genmed"]/text()').extract()
        post_info = post_information[0].encode('utf8')
        percentage_of_total_warez_posts = post_info[:post_info.index("%")]
        posts_per_day = post_info[post_info.index("%") + 18: post_info.index("posts")]
        occupation = rows[4].xpath("div[@class='icon']/span/text()").extract()
        intrests = rows[5].xpath("div[@class='icon']/span/text()").extract()
        poster_rank = rows[6].xpath("div[@class='icon']/span/img/@title").extract()

        item['percentage_of_total_warez_posts'] = percentage_of_total_warez_posts
        item['posts_per_day'] = posts_per_day.strip()
        item['occupation'] = occupation[0].strip()
        item['intrests'] = intrests[0].strip()
        item['poster_rank'] = poster_rank[0].strip()

        yield item



