# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class News(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    author_name = scrapy.Field()
    raw_content = scrapy.Field()
    published_at = scrapy.Field()
    media_id = scrapy.Field()

