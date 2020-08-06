import scrapy


class PostSpider(scrapy.Spider):
    name = "pages"
    start_urls = [
        'https://www.siteinspire.com/',
    ]
# Passes the URL of each post

    def parse(self, response):
        for post in response.css('div.thumbnail'):
            url = post.css('.wrapper .image a::attr(href)').get()

            if url is not None:
                url = response.urljoin(url)
                yield response.follow(url, callback=self.fillCategory)
# After reading the first page, navigate to the next Page
        next_page = response.css('.pagination .next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

# Custom method classthat access each post
    def fillCategory(self, response):
        if response.css('[id="main"]') is not None:
            for item in response.css('[id="main"]'):
                yield{
                    'Title': item.css('h1::text').get(),
                    'Site-URL': response.xpath(
                        '//*[@id="website"]/div[2]/div'
                        '/ul[1]/li[1]/a/span[2]/text()')
                    .extract_first(),
                    'Categories': item.css('.context ul li a::text')[0].get()
                }