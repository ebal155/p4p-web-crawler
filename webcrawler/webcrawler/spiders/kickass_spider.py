
import scrapy
from webcrawler.items import KickassItem


class KickassSpider(scrapy.Spider):
    """Spider used to parse post pages in kickass.to"""
    name = "kickass"
    allowed_domains = ["https://kickass.to/"]

    start_urls = ["https://kickass.to"]

    #Read off the kickass API and parse all the links with parse_movie_page as a callback
    def parse(self, response):

        list_links = []
        #The kickass data dump can be separated into smaller files using blockcreator.py
        filename = "moviedumpblocks/test6.txt"  # list of links that will be read from

        with open(filename) as f:
            for line in f:
                line = line.split("|")
                list_links.append((line[3], line[5], line[10]))
                # make an item and store the data
                # pass it in

            for link in list_links:
                request = scrapy.Request(url=link[0], callback=self.parse_movie, dont_filter=True)

                request.meta['file_size'] = link[1]  # bytes
                request.meta['post_date'] = link[2]  # UNIX timestamp

                yield request

    #Make a request to a movie page, and scrape the relevant information
    def parse_movie(self, response):

        item = KickassItem()

        title = response.xpath(".//h1[@class='novertmarg']/a/span/text()").extract()
        title = title[0]

        author = response.xpath(".//div[@class='font11px lightgrey line160perc']/span/span/a/text()").extract()
        if len(author) != 0:
            author = author[0]
        else:
            author = "N/A"

        author_reputation = response.xpath(".//div[@class='font11px lightgrey line160perc']/span[@class='badgeInline']/span[@class='repValue positive']/text()").extract()
        if len(author_reputation) != 0:
            author_reputation = author_reputation[0]
        else:
            author_reputation = "N/A"

        downloads = response.xpath(".//div[@class='font11px lightgrey line160perc']/text()").extract()
        for x in range(0, len(downloads)):
            if("Downloaded" in downloads[x]):
                downloads = downloads[x].split("Downloaded")[1].split("times")[0].strip()

        replies = response.xpath(".//div[@class='tabs tabSwitcher']/ul[@class='tabNavigation']/li/a/span/i/text()").extract()
        if len(replies) != 0:
            replies = replies[0]
        else:
            replies = "0"

        likes = response.xpath(".//span[@id='thnxCount']/span/text()").extract()
        if len(likes) != 0:
            likes = likes[0]
        else:
            likes = "0"

        dislikes = response.xpath(".//*[@id='fakeCount']/span/text()").extract()
        if len(dislikes) != 0:
            dislikes = dislikes[0]
        else:
            dislikes = "0"

        seeders = response.xpath("//div[@class='seedLeachContainer']/div[@class='seedBlock']/strong/text()").extract()
        if len(seeders) != 0:
            seeders = seeders[0]
        else:
            seeders = "0"

        leechers = response.xpath("//div[@class='seedLeachContainer']/div[@class='leechBlock']/strong/text()").extract()
        if len(leechers) != 0:
            leechers = leechers[0]
        else:
            leechers = "0"

        #Non-common metadata
        imdb_rating = response.xpath("//*[@id='tab-main']/div[2]/div/ul[1]/li[4]/text()").extract()
        if len(imdb_rating) != 0:
            imdb_rating = imdb_rating[0]
        else:
            imdb_rating = "No rating"

        detected_quality = response.xpath(".//div[@class='dataList']/ul[@class='block overauto botmarg0']/li[2]/span/text()").extract()
        if len(detected_quality) != 0:
            detected_quality = detected_quality[0]
        else:
            detected_quality = "N/A"

        movie_release_date = response.xpath("//*[@id='tab-main']/div[2]/div/ul[2]/li[2]/text()").extract()
        if len(movie_release_date) != 0:
            movie_release_date = movie_release_date[0]
        else:
            movie_release_date = "N/A"

        language = response.xpath(".//div[@class='dataList']/ul[2]/li[4]/span/text()").extract()
        if len(language) != 0:
            language = language[0].strip()
        else:
            language = "N/A"

        genre = response.xpath(".//div[@class='dataList']/ul[@class='block overauto botmarg0']/li[6]/a[@class='plain']/span/text()").extract()

        file_size = response.meta['file_size']

        post_date = response.meta['post_date']

        cast = response.xpath("//*[@id='tab-main']/div[2]/div/div[1]/span/a/text()").extract()

        item["title"] = title
        item["author"] = author
        item["author_reputation"] = author_reputation
        item["downloads"] = downloads
        item["post_date"] = post_date
        item["replies"] = replies
        item["likes"] = likes
        item["dislikes"] = dislikes
        item["seeders"] = seeders
        item["leechers"] = leechers
        item["imdb_rating"] = imdb_rating
        item["detected_quality"] = detected_quality
        item["movie_release_date"] = movie_release_date
        item["language"] = language
        item["genre"] = genre
        item["file_size"] = file_size
        item["cast"] = cast

        yield item
