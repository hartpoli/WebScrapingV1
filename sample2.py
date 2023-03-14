import scrapy

class MySpider(scrapy.Spider):
    name = "my_spider"
    allowed_domains = ["example.com"]
    start_urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        # add more URLs here
    ]

    def parse(self, response):
        # extract data from the current page
        data = {
            'title': response.css('h1::text').get(),
            'body': response.css('div.article-body::text').getall(),
            'author': response.css('span.author::text').get(),
            'date_published': response.css('span.date-published::text').get(),
        }
        yield data

        # follow links to other pages
        for link in response.css('a::attr(href)').getall():
            if 'example.com' in link:
                yield response.follow(link, self.parse)

        # follow links to other websites
        for link in response.css('a::attr(href)').getall():
            if 'example2.com' in link:
                yield scrapy.Request(link, callback=self.parse_other_website)

    def parse_other_website(self, response):
        # extract data from the other website
        data = {
            'title': response.css('h1::text').get(),
            'body': response.css('div.article-body::text').getall(),
            'author': response.css('span.author::text').get(),
            'date_published': response.css('span.date-published::text').get(),
        }
        yield data