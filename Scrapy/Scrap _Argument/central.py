# -*- coding: utf-8 -*-
import scrapy


class CentralSpider(scrapy.Spider):
    name = 'central'
    allowed_domains = ['classcentral.com']
    start_urls = ['https://classcentral.com/subjects/']

    def __init__ (self, subject=None):
        self.subject = subject

    def parse(self, response):
        if self.subject:
            subject_url = response.xpath('//a[contains(@title," '+ self.subject +' ")]/@href').get()
            yield response.follow(url = subject_url, callback = self.parse_subject)
        
        else:
            self.log("Scraping All BOOKS")
            subjects =  response.xpath('//h3/a[1]/@href').getall() 
            for subject in subjects:
                yield response.follow(url = subject, callback = self.parse_subject)
                    
    def parse_subject(self, response):
        name = response.xpath("//h1[@class='head-1']/text()").get()

        courses = response.xpath('//tr[@itemtype="http://schema.org/Event"]')
        for course in courses:
            name = course.xpath('normalize-space(.//span[@itemprop="name"]/text())').get()
            university = course.xpath('normalize-space(.//div[@class="truncate"]/a/text())').get() 
            link = course.xpath('//a[@itemprop="url"]/@href').get()
            ab_link = response.urljoin(link)   
            site_name = course.xpath('normalize-space(.//span/a[@title="List of  MOOCs"]/text())').get()
            duration = course.xpath('normalize-space(.//span/following-sibling::span/text())').get() 

            yield{
                'Name': name,
                'University': university,
                'Link' :ab_link,
                'WebSite' :site_name,
                'Duration':duration
            } 
    