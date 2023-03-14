import scrapy
from datetime import datetime

class ArticleSpider(scrapy.Spider):
    name = 'article_scraper'
    start_urls = ['https://example.com/articles']

    def parse(self, response):
        for article in response.css('div.article'):
            yield {
                'title': article.css('a.article-title::text').get(),
                'author': article.css('span.author::text').get(),
                'date_published': datetime.strptime(article.css('span.date-published::text').get(), '%Y-%m-%d').date()
            }
        
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
