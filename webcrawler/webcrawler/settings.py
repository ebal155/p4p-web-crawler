# -*- coding: utf-8 -*-

# Scrapy settings for webcrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'webcrawler'

SPIDER_MODULES = ['webcrawler.spiders']
NEWSPIDER_MODULE = 'webcrawler.spiders'
DOWNLOADER_MIDDLEWARES = {
'webcrawler.middleware.middleware': 302,
}	

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'webcrawler (+http://www.yourdomain.com)'
