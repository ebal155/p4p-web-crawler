# p4p-web-crawler
Web crawler written for part 4 project

How to use:
Go to top level webcrawler directory in command line

scrapy crawl [spider_name] -o [file_name].json 

[spider_name] is defined inside the spider.py file as a variable called "name"
[file_name] can be whatever you want

eg. for kickass_spider, 
scrapy crawl kickass -o items.json 

Current spiders:
kickass (kickass_spider)
warezbb (warezbb_spider)

