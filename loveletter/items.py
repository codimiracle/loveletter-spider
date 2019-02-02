# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class LoveTheme(scrapy.Item):
    episode = scrapy.Field()
    subject = scrapy.Field()
    title = scrapy.Field()

    @property
    def id(self):
        pass


class LoveLetter(scrapy.Item):
    sender = scrapy.Field()
    receiver = scrapy.Field()
    body = scrapy.Field()

    @property
    def id(self):
        pass
