# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ImmageNameItem(scrapy.Item):
   Name = scrapy.Field()
   Price = scrapy.Field()
   # when using the images pipeline, items must define both the image_urls and the images field. 
   image_urls = scrapy.Field()
   images = scrapy.Field()
