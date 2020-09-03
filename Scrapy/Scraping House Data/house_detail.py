# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'house_detail'
    allowed_domains = ['newyork.craigslist.org']
    start_urls = ['https://newyork.craigslist.org/d/housing-swap/search/swp']

    def parse(self, response):
        rows = response.xpath("//li[@class='result-row'] ")
        for row in rows:
            data = row.xpath('.//p/time[@class="result-date"]/@datetime').get()
            link = row.xpath('.//a[@class="result-title hdrlnk"]/@href').get()
            text = row.xpath('.//a[@class="result-title hdrlnk"]/text()').get() 

            yield response.follow(url =link, callback = self.parse_listing, 
                                meta={'Data':data, 'Link':link, 'Text':text}) 

            # yield scrapy.Request(url =link, callback=self.parse_country, 
                                   #meta={'Data':data,'Link':link,'Text':text})
        # next page
        next_page = response.xpath('//a[@class="button next"]/@href').get()
        yield response.follow(url = next_page, callback = self.parse) # [3]

    def parse_listing(self, response):
        Data = response.request.meta['Data'] # resposne.meta['Date'] 
        Link = response.request.meta['Link'] # response.meta['Link']
        Text = response.request.meta['Text'] # response.meta['Text']

        content = response.xpath('normalize-space((//section[@id="postingbody"]/text())[2])').get() 
        #image_1 = response.xpath('(//div[@class="swipe-wrap"]//img/@src)[1]').get()
        images = response.xpath('//div//img/@src').getall()  
        image_1 =[image.replace('50x50c','600x450')for image in images]
        new_im = image_1[1:]
        a       = response.xpath('//span[@class="shared-line-bubble"]/b/text()').getall()    
        status = response.xpath('//span[@data-today_msg="available now"]/text()').get() 
        address = response.xpath('//div[@class="mapaddress"]/text()').get()

        yield{
            'Data': Data,
            'Link': Link,
            'Text': Text,
            'Content' :content,
            'Images' :new_im,
            'Area'    :a, 
            'Status'  :status, 
            'Address' :address
        }          