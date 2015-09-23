# p4p-web-crawler
These web crawlers and analysers were built for our part four project at the University of Auckland. Our project was titled  Online Piracy: Analyzing copyright infringement on the Internet. The objective of the project was to  perform an empirical study to understand how copyrighted content(e.g., movies and TV shows) are disseminated using two network application architectures: P2P (BitTorrent) and Web (File Hosting Services). We performed screen scrapes of two major P2P and File hosting Indexing websites to collect data about the content being shared, the usernames of the person publishing the content,
Web crawlers and analysers written for our part 4 project at the University of Auckland. 

### Running the Web Crawlers
--------

  Install Scrapy 
    
    available at http://scrapy.org/download/  
Go to top level webcrawler directory and run the command below:

    scrapy crawl [spider_name] -o [file_name].json 

[spider_name] is defined inside each spider.py file as a variable called "name".  
[file_name] is the output filename which can be specified any of the supported output formats.  
Supported output formats in Scrapy: XML, CSV or JSON

eg. for kickass_spider

    scrapy crawl kickass -o items.json 

Current spiders:  
* kickass (kickass_spider.py)  
* warez_link (warezbb_top_100_posters.py)  
* warez_thread_parser (warezbb_thread_link_parser_spider.py)  
* top_100 (warez_bb_top_100_posters.py)  

### Analysing the collected data:
-----
The post processing scripts were run on the raw data that was collected using the web crawlers  
* post_process_kickass_results.py  
* post_process_warezbb_results.py  

We perform analysis on the processed data using two analyser scripts:  
* kickass_data_analyser.py  
* warezbb_data_analyser.py  

The methods in these analyser scripts use the utility methods from analyser.py, which is a utility library that helps query the csv files. The methods also use the printing methods from my_printer.py to output the results in different formats.

The data we collected is available with our supervisor. Contact details are listed below

    a.mahanti@auckland.ac.nz

### Results
-----
The following items can be found under data.rar (separated for kickass and warezbb):  
* Raw metadata that was collected can be found under the 'data' folder (run the post-processing scripts to process this data)  
* The links that were traversed by both web crawlers are inside the 'links' folder  
* Various csv tables that were made using the analysis library are inside the 'tables' folder  
* Graphs that were made using R are located inside the 'R graphs' folder  

