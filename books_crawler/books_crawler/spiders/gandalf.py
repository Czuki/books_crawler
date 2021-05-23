import scrapy
from scrapy.spiders import SitemapSpider

from ..items import BookItem


class GandalfSpider(SitemapSpider):
    name = 'gandalf'
    allowed_domains = ['gandalf.com.pl']
    start_urls = ['https://www.gandalf.com.pl/']
    sitemap_urls = [
        'https://www.gandalf.com.pl/files/sitemaps/produkty_ksiazki_2.xml',
        # 'https://www.gandalf.com.pl/files/sitemaps/osoby_2.xml',
        # 'https://www.gandalf.com.pl/files/sitemaps/osoby_3.xml',
        # 'https://www.gandalf.com.pl/files/sitemaps/osoby_4.xml',
        # 'https://www.gandalf.com.pl/files/sitemaps/osoby_5.xml',
        # 'https://www.gandalf.com.pl/files/sitemaps/osoby_6.xml',
    ]

    def parse(self, response):

        book = BookItem()
        title = response.css('h1.title::text').get().strip()

        product_details_list = response.css('#product-details ul')
        isbn = product_details_list.css('li:nth-child(7) span:nth-child(2)::text').get().strip()

        book['name'] = title.strip('(miękka)').strip('(twarda)')
        book['isbn'] = isbn
        book['author'] = response.css('div.author::attr(title)').get().strip()

        yield book
