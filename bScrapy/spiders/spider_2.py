#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import scrapy
import urllib
import logging
import requests
from random import uniform
from lxml import etree
from scrapy.spiders import CrawlSpider, Rule
from bScrapy.items import HomeItem

START_URL = "http://bj.lianjia.com/ershoufang/"
SLEEP_TIME = 2
global_cnt = 0;

COMMON_HEADER = {
    "Proxy-Connection" : "keep-alive",
    "Cache-Control" : "max-age=0",
    "Upgrade-Insecure-Requests" : "1",
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "DNT" : "1",
    "Accept-Encoding" : "gzip, deflate, sdch",
    "Accept-Language" : "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ru;q=0.2,es;q=0.2",
}

class ScrapyVersion2(CrawlSpider):
    name = "Spider_2"
    district_list = ['dongcheng', 'xicheng', 'chaoyang', 'haidian', 'fengtai', 'shijingshan', 'tongzhou', 'changping', ]
    home_id_list = []

    def __del__(self):
        global global_cnt
        print "Done: %d" % (global_cnt)
        
    def start_requests(self):
        global global_cnt
        logging.info ("start crawl LianJian site.");
        tmp_head = COMMON_HEADER;
        tmp_head["Host"] = "bj.lianjia.com"
        for district_name in self.district_list:
            url = "http://bj.lianjia.com/ershoufang/%s/" % (district_name);
            yield scrapy.Request (url, headers = tmp_head, callback = self.workCallback)
            time_1 = SLEEP_TIME + uniform (0,2);
            time.sleep (time_1)
            global_cnt += 1
            
    def workCallback(self, response):
        global global_cnt
        if response.status is 200:
            base_url = response.url;
            tmp_head = COMMON_HEADER
            tmp_head["Host"] = 'bj.lianjia.com'
            
            for i in range (1, 101):
                new_url = "%spg%d/" % (base_url, i)
                time_1 = SLEEP_TIME + uniform (0, 2);
                time.sleep (time_1)
                yield scrapy.Request (new_url, headers = tmp_head, callback = self.pageCallback)
                global_cnt += 1
        else:
            logging.error ("failed");
            
    def pageCallback(self, response):
        if response.status is 200:
            home_list = response.xpath("/html/body/div[4]/div[1]/ul/li")
            item = HomeItem ()
            for home in home_list:
                title = home.xpath ("div[1]/div[1]/a//text()").extract_first ()
                hid = home.xpath ("div[2]/div[1]/@data-hid").extract_first ()
                address = home.xpath ("div[1]/div[2]/div/a//text()").extract_first ()
                price = home.xpath ("div[1]/div[6]/div[1]/span//text()").extract_first ()

#                if hid in self.home_id_list:
#                   continue
#                self.home_id_list.append (hid)

                item["title"] = title
                item["address"] = address
                item["price"] = price
                item["hid"] = hid
                yield item
        else:
            logging.error ("request page: %s failed %s", response.url, response.status);
