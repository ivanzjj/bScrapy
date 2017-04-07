#!/usr/bin/env python
# -*- coding:utf-8 -*-

import scrapy
import urllib
import logging
from bScrapy.items import SynonymItem
from scrapy.spiders import CrawlSpider, Rule

BAIDU_URL = "https://www.baidu.com"
BAIDU_HANYU = "http://hanyu.baidu.com"
COMMON_HEADER = {
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "DNT": "1",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ru;q=0.2,es;q=0.2",
}
QUERY_WORD = ["生日"]

class ScrapyVersion1(CrawlSpider):
    name = "Spider_1"
    def start_requests(self):
        logging.info ("get baidu homepage success.")
        tmp_head = COMMON_HEADER
        tmp_head["Host"] = "hanyu.baidu.com"
        for word in QUERY_WORD:
            arg_1 = {"wd": word};
            new_url = "%s/s?%s" % (BAIDU_HANYU, urllib.urlencode (arg_1))
            yield scrapy.Request(new_url, headers=tmp_head, callback=self.recv_query)
            
    def recv_query(self, response):
        if response.status is 200:
            original_word = response.xpath ('//div[@id="pinyin"]/h2/strong/text()').extract_first()
            synonym_list = response.xpath ('//div[@id="synonym"]/div/a/text()').extract ()
            item = SynonymItem ()
            item['original_word'] = original_word
            item['synonym_words'] = []
            idx = 0
            for word in synonym_list:
                item['synonym_words'].append(word)
            return item
        else:
            logging.error ("query word failed and status is %s" % (response.status))

