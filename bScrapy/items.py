# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class SynonymItem(scrapy.Item):
    original_word = scrapy.Field ()
    synonym_words = scrapy.Field ()

class HomeItem(scrapy.Item):
    title = scrapy.Field ()
    address = scrapy.Field ()
    price = scrapy.Field ()
    hid = scrapy.Field ()
