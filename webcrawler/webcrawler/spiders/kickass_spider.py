
import scrapy
import sys, traceback
from webcrawler.items import KickassItem

class KickassSpider(scrapy.Spider):
    name = "kickass"
    allowed_domains = ["https://kickass.to/"]

    start_urls = [
       "https://kickass.to"
    ]

    # grep -c \|Movies\| "dailydump.txt"

    #Read off the dump made with dumpseparator and parse all the links with parse_movie_page as a callback
    def parse(self, response):

        list_links = []
        filename = "moviedump.txt"

        with open(filename) as f:

            for line in f:
                line = line.split("|")
                list_links.append(line[3])
                # make an item and store the data
                # pass it in

            for link in list_links:
                yield scrapy.Request(url=link, callback=self.parse_movie, dont_filter=True)


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
        for x in range(0,len(downloads)):
            if("Downloaded" in downloads[x]):
                downloads = downloads[x].split("Downloaded")[1].split("times")[0].strip()

        post_date = response.xpath(".//div[@class='font11px lightgrey line160perc']/text()").extract()
        post_date = post_date[0].split("Added on")[1].split("by")[0].strip()

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


        #Non - common metadta
        imdb_rating = response.xpath("//*[@id='tab-main']/div[2]/div/ul[1]/li[4]/text()").extract()
        if len(imdb_rating) != 0:
            imdb_rating = imdb_rating[0]
        else:
            imdb_rating = "No rating"

        # rotten_tomatoes = response.xpath("//*[@id='tab-main']/div[2]/div/ul[1]/li[5]/span[1]").extract()
        # rotten_tomatoes = rotten_tomatoes[0] #43 exceptions
        # except:
        #     f = open('test','a')
        #     exc_type, exc_value, exc_traceback = sys.exc_info()
        #     f.write(title + "\n" + str(language) + "\n")
        #     f.close()
        
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

        #Getting the unit of file_size, e.g. GB,MB,etc.
        file_size_unit = response.xpath("//*[@id='tab-main']/div[5]/div[1]/div[1]/strong/span/text()").extract()
        file_size = response.xpath("//*[@id='tab-main']/div[5]/div[1]/div[1]/strong/text()").extract()

        if (len(file_size_unit) and len(file_size_unit)) != 0:
            file_size = file_size[0] + file_size_unit[0]
        else:
            file_size = "N/A"

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
        #item["rotten_tomatoes"] = rotten_tomatoes
        item["detected_quality"] = detected_quality
        item["movie_release_date"] = movie_release_date
        item["language"] = language
        item["genre"] = genre
        item["file_size"] = file_size
        item["cast"] = cast

        yield item