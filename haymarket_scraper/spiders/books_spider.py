import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"

    def start_requests(self):
        urls = [
            'https://www.haymarketbooks.org/books'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for book in response.css('.edition_item'):
            yield {
                'title': book.css('.title::text').get(),
                'contributors': book.css('.contributors a::text').getall(),
                'teaser': ''.join(book.css('.teaser ::text').getall())
            }
        next_page = response.css('a.next_page::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
