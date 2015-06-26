from urlparse import urlparse
import scrapy

class middleware(object):
	def process_response(self, request, response, spider):
		o = urlparse(response.url)
		if o.hostname == "www.warez-bb.org":
			if ("/login.php" in o.path) and ("redirect" in o.query):
				print "!@! logging in again"
				spider.start_page = spider.curr_page
				spider.curr_page = 0
				return scrapy.FormRequest.from_response(
					response,
					formdata={'username': 'nzgangster', 'password': 'KANyezus'},
					dont_filter=True
					)
			return response
		else:
			return response