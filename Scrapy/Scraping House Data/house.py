# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['newyork.craigslist.org']
    start_urls = ['https://newyork.craigslist.org/d/housing-swap/search/swp']

    def parse(self, response):
        rows = response.xpath("//li[@class='result-row'] ")
        for row in rows:
            yield{
                'data':row.xpath('.//p/time[@class="result-date"]/@datetime').get(),
                      #row.xpath('//li/p/time[@class="result-date"]/@title').get(),
                'link':row.xpath('.//a[@class="result-title hdrlnk"]/@href').get(),
                'text':row.xpath('.//a[@class="result-title hdrlnk"]/text()').get() 
            }
        # next page
        next_page = response.xpath('//a[@class="button next"]/@href').get()
        yield response.follow(url = next_page, callback = self.parse) # [3]
