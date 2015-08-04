import scrapy
import sys
import re
from webcrawler.items import WarezbbItem

class warezbb_link_checker_spider(scrapy.Spider):
    name = "warezLink_checker"
    allowed_domains = ["https://www.warez-bb.org/*"]
    download_delay = 6
    start_urls = [
       "https://www.warez-bb.org/login.php"
    ]
    curr_page = 0
    start_page = 125001
    end_thread = 130186 #130186

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
            with open("linksWarezbb_noDupilcates2.txt","r") as f:
                count = 0
                for line in f:
                    if count >= self.start_page and count <= self.end_thread:
                        file2 = open("currentPos.txt","w")
                        file2.write(str(count))
                        file2.close()
                        words = line.split()
                        link = words[0]
                        views = words[1]
                        replies = words[2]
                        item = WarezbbItem()
                        item['replies'] = replies
                        item['views'] = views
                        item['link'] = link
                        yield scrapy.Request(url=link,meta={'item':item},
                            callback=self.parse_thread, dont_filter=True,priority=-1)
                    count = count + 1

    def parse_thread(self, response):
        item = response.meta['item']
        title = response.xpath(".//div[@class='topic-view']/div[@class='heading']/a/text()").extract()
        item['title'] = title[0]
        item['sources'] = self.get_movie_sources(title[0])
        item['detected_quality'] = self.get_movie_quality(title[0])

        author = response.xpath(".//div[@class='author']/strong/text()")
        author = author.extract()
        item['author'] = author[0]

        post_date = response.xpath(".//div[@class='date']/a/text()").extract()
        post_date = post_date[0]
        item['post_date'] = post_date

        codes = response.xpath(".//div[@class='code']/span/text()")
        codes = codes.extract()
        codes_to_add = []
        for code in codes:
            if ("http" in code) and ( "imdb" not in code):
                codes_to_add.append(code)
        item['code_fields'] = codes_to_add
        yield item

    def get_movie_sources(self, title):
        found = re.search('^\[(.*?)\]', title)
        if found: 
            sources = found.group(1)
            if "/" in sources:
                char_to_spilt_by = "/"
            elif "+" in sources:
                char_to_spilt_by = "+"
            elif "\\" in sources:
                char_to_spilt_by = "\\"
            elif "|" in sources:
                char_to_spilt_by = "|"
            elif "-" in sources:
                char_to_spilt_by = "-"
            else:
                char_to_spilt_by = None
        else: 
            return None
        if char_to_spilt_by is not None:
            return sources.split(char_to_spilt_by)
        else:
            return [sources]

    def get_movie_quality(self, title):
        quality_types = [ 
            "dvdrip", "bdrip",
            "dvdsrc", "telesync",
            "bluray", "dbd",
            "cam", "hdts",
            "tc", "telecine",
            "ppv", "webrip",
            "vodrip", "workprint",
            "screener", "hdrip",
            "720p", "web-dl",
            "1080p", "hdtv",
            "480p", "web dl",
            "brrip", "mp4"
            ]
        title = title.lower()
        movie_quality_array = []
        for type_ in quality_types:
            if type_ in title:
                movie_quality_array.append(type_)

        return movie_quality_array
