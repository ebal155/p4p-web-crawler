# p4p-web-crawler
Web crawlers and analysers written for part 4 project.

To run the web crawlers:  
Install Scrapy from http://scrapy.org/download/  
Go to top level webcrawler directory and run this command:

scrapy crawl [spider_name] -o [file_name].json 

[spider_name] is defined inside the spider.py file as a variable called "name".  
[file_name] is the output filename which can be specified any of the supported output formats.  
Supported output formats in Scrapy: XML, CSV or JSON

eg. for kickass_spider,  
scrapy crawl kickass -o items.json 

Current spiders:  
kickass (kickass_spider.py)  
warez_link (warezbb_top_100_posters.py)  
warez_thread_parser (warezbb_thread_link_parser_spider.py)  
top_100 (warez_bb_top_100_posters.py)  

