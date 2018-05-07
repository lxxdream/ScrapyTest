# -*- coding: utf-8 -*-
import scrapy
from quotestest.items import QuotestestItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        #print(response.text)
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuotestestItem()
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tag::text').extract()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item

        next = response.css('.pager .next a::attr(href)').extract_first()
        nexturl = response.urljoin(next)
        yield scrapy.Request(url=nexturl, callback=self.parse)
