import scrapy
from webcrawler.items import warezbbItem
#KANyezus
class warezbbSpider(scrapy.Spider):
    name = "warezbb"
    allowed_domains = ["https://www.warez-bb.org/"]
    start_urls = [
       "https://www.warez-bb.org/login.php"
    ]

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'nzgangster', 'password': 'KANyezus'},
            callback=self.after_login, dont_filter=True
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.log("Login failed", level=log.ERROR)
            return
        else:
            print "Logged in"