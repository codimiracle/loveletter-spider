# -*- coding: utf-8 -*-

# Define here the item loaders for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/loaders.html

from scrapy.loader import ItemLoader
from items import LoveLetter, LoveTheme

class LoveLetterLoader(ItemLoader):
    def __init__(self, response=None):
        super().__init__(item=LoveLetter(), response=response)

class LoveThemeLoader(ItemLoader):
    def __init__(self, response=None):
        super().__init__(item=LoveTheme(), response=response)
    