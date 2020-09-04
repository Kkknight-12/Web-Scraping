# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from immage_name.items import ImmageNameItem
from PIL import Image

def product_info(response, value):
    return response.xpath('//tr/th[text()="'+value+'"]/following-sibling::td/text()').get()

class ImageNameSpider(scrapy.Spider):
    name = 'image_name'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/index.html']

    def parse(self, response):
        books = response.xpath('//h3/a') # common link for all books

        for links in books: 
            link = links.xpath(".//@href").get() # looping over each link one by one
            yield response.follow(url = link, callback = self.parse_books) 

    def parse_books(self, response):
        l = ItemLoader(item = ImmageNameItem(), response= response) #[1]

        Name  = response.xpath('//h1/text()').get(),
        Price =  product_info(response,'Price (excl. tax)'),
        image_urls = response.urljoin(response.xpath("//img/@src").get()),  
      
        l.add_value('Name',Name) # [2]
        l.add_value('Price',Price) # [2]
        l.add_value('image_urls',image_urls) # [2]
        return l.load_item()  # [2]