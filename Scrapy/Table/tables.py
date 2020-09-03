# -*- coding: utf-8 -*-
import scrapy


class TablesSpider(scrapy.Spider):
    name = 'tables'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population']

    def parse(self, response):
        table = response.xpath("//table[contains(@class, 'wikitable sortable')]")[0] 
        rows = table.xpath(".//tr")[1:] # zero element is header so skipping it
        for row in rows:
            rank = row.xpath(".//td[1]/text()").get().strip()
            name = row.xpath(".//td[2]//text()").get()
            state = row.xpath(".//span[@class='flagicon']/following-sibling::a/text()|"
                               ".//span[@class='flagicon']/following-sibling::text()").get() 
          

            yield{
                "Name":name,
                "Rank":rank,
                "State":state
            }
