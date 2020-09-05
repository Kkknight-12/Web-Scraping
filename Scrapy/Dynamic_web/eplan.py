# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest

class EplanSpider(scrapy.Spider):
    name = 'eplan'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://www.eplanning.ie/']

    def parse(self, response):
        urls = response.xpath('//td/a/@href').getall()[1:]  
        # urls contain some # signs 
        for url in urls:
            if "#" == url:
                pass
            else:
                yield scrapy.Request(url, callback = self.parse_application)
    
    def parse_application(self, response):
        app_url = response.xpath(
            "//span[@class='glyphicon glyphicon-inbox btn-lg']/following-sibling::a/@href").get() 
        yield response.follow(url = app_url, callback = self.parse_form)
    
    def parse_form(self, response):
        yield FormRequest.from_response(response, 
                                        formdata={'RdoTimeLimit':'42'},
                                        dont_filter = True, 
                                        formxpath = '(//form)[2]',
                                        callback=self.parse_pages)

    def parse_pages(self, response):
        app_url = response.xpath("//td/a/@href").getall()
        for url in app_url:
            yield response.follow(url =url, callback = self.parse_items)
        
        next_page = response.xpath("//a[@rel = 'next']/@href").get()
        yield response.follow(url = next_page, callback = self.parse_pages)

    def parse_items(self, response):
        agent_btn = response.xpath("*//input[@value = 'Agents']/@style").get()  

        if 'display: inline;  visibility: visible;' in agent_btn:
            name = response.xpath("//tr[th = 'Name :']/td/text()").get() 
            first_add = response.xpath("//tr[th = 'Address :']/td/text()").getall()
            sec_add = response.xpath("//tr[th = 'Address :']/following-sibling::tr/td/text()").getall()[0:3]  
            address = first_add + sec_add
            phone = response.xpath("//tr[th = 'Phone :']/td/text()").get()
            fax=   response.xpath("//tr[th = 'Fax :']/td/text()").get()
            email = response.xpath("//tr[th = 'e-mail :']/td/a/text()").get()
            url = response.url

            yield{
                'Name':name,
                'Address':address,
                'Phone':phone,
                'Fax':fax,
                'E-mail':email,
                'Url':url
            }
        
        else:
            self.logger.info('Agent button not found on page, passing invalid url')

