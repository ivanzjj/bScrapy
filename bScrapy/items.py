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


# definition for Spider_2

class HomeItem(scrapy.Item):
    title = scrapy.Field ()
    address = scrapy.Field ()
    prices = scrapy.Field ()
    dates = scrapy.Field ()
    hid = scrapy.Field ()

class NewItem(scrapy.Item):
    title = scrapy.Field ()
    address = scrapy.Field ()
    prices = scrapy.Field ()
    dates = scrapy.Field ()
    hid = scrapy.Field ()

# end of definition for Spider_2     
    
