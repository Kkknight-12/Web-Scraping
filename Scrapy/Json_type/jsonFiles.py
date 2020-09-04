# -*- coding: utf-8 -*-
import scrapy
import json

class JsonfilesSpider(scrapy.Spider):
    name = 'jsonFiles'
    allowed_domains = ['trumptwitterarchive.com/']
    start_urls = ['http://d5nxcu7vtzvay.cloudfront.net/data/realdonaldtrump/2017.json']

    def parse(self, response):
        resp = json.loads(response.body)

        for tweet in resp:
            yield{
                   'source': tweet ['source'],
                   'id_str': tweet['id_str'],
                   'text': tweet['text'],
                   'created_at': tweet['created_at'],
                   'retweet_count':tweet ['retweet_count'],
                   'in_reply_to_user_id_str':tweet['in_reply_to_user_id_str'],
                   'favorite_count': tweet['favorite_count'],
                   'is_retweet': tweet['is_retweet']
                }
