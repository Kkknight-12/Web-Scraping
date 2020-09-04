# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector # need selector to change the page
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys


class ExampleSpider(scrapy.Spider):
    name = 'example'

    def start_requests(self):
        yield SeleniumRequest(
            url='https://duckduckgo.com',
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):
        img = response.meta['screenshot']

        with open('screenshot.png', 'wb') as f:
            f.write(img)
        """ 
        to be able to select the element we need a driver
        """
        driver = response.meta['driver']
        search_input = driver.find_element_by_xpath("(//input[contains(@class, 'js-search-input')])[1]")
        search_input.send_keys('Hello World')

        search_input.send_keys(Keys.ENTER)
        """
        now we need to perform our search on the hello world search page for which we need to 
        take the response form the driver object[line 25] and convert it to selector object, 
        for the same reason we are importing the selector on line 3
        """
        html = driver.page_source 
        response_obj = Selector(text=html)

        # extracing all the link on the opened web page with the help of loop
        # response_obj is used instead of response.xpath to perform extraction on hello world result page
        links = response_obj.xpath("//div[@class='result__extras__url']/a")
        for link in links:
            yield {
                
                'URL': link.xpath(".//@href").get()
            }
