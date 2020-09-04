# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

class ImmageNamePipeline(object):
    def process_item(self, item, spider):
        os.chdir('/Users/knight/Desktop/delicous/im')

        if item['images'][0]['path']:
            new_image_name = item['Name'][0] + '.jpg'
            new_image_path = 'full/' + new_image_name

            os.rename(item['images'][0]['path'], new_image_path)
    
"""
This is what look like - dictionary
{'Name': ["Shakespeare's Sonnets"],
 'Price': ['£20.66'],
 'image_urls': ['http://books.toscrape.com/media/cache/4d/7a/4d7a79a8be80a529b277ed5c4d8ba482.jpg'],
 'images': [{'checksum': '6764521cdae360de611d12a16884bfdd',
             'path': 'full/887930c21dc5052222d22ab613500fd2bddf0805.jpg',
             'url': 'http://books.toscrape.com/media/cache/4d/7a/4d7a79a8be80a529b277ed5c4d8ba482.jpg'}]}

here item['images'][0]['path'] is the " 'path': 'full/887930c21dc5052222d22ab613500fd2bddf0805.jpg' "
so the are saying that if you find this above path thing in items then change 
the name with help of os.rename  with custome defined new_image_name
"""