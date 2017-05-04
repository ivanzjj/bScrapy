#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import scrapy
import urllib
import logging
import requests
import csv
import datetime
from random import uniform
from lxml import etree
from scrapy.spiders import CrawlSpider, Rule
from bScrapy.items import *

START_URL = "http://bj.lianjia.com/ershoufang/"
SLEEP_TIME = 2
LAST_DATA_FILE = "old.csv"

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

    id_map = []

    old_data_map = {}

    def __init__(self):
        logging.info ("Loading Last data......")
        with open(LAST_DATA_FILE, "r") as fp:
            csv_reader = csv.DictReader (fp)
            for row in csv_reader:
                print type (row), row
                id_ = row['hid']
                self.old_data_map[id_] = []
                self.old_data_map[id_].append (row['prices'].split(','))
                self.old_data_map[id_].append (row['dates'].split(','))
                self.old_data_map[id_].append (row['title'])
                self.old_data_map[id_].append (row['address'])

        print "Len: %d" % (len(self.old_data_map))

    def closed (self, reason):
        print "Old_data_map: %d" % (len (self.old_data_map))
        
        
    def start_requests(self):
        logging.info ("start crawl LianJian site.");
        tmp_head = COMMON_HEADER;
        tmp_head["Host"] = "bj.lianjia.com"
        for district_name in self.district_list:
            url = "http://bj.lianjia.com/ershoufang/%s/" % (district_name);
            yield scrapy.Request (url, headers = tmp_head, callback = self.workCallback)
            time_1 = SLEEP_TIME + uniform (0,2);
            time.sleep (time_1)
            
    def workCallback(self, response):
        if response.status is 200:
            base_url = response.url;
            tmp_head = COMMON_HEADER
            tmp_head["Host"] = 'bj.lianjia.com'
            
            for i in range (1, 2):
                new_url = "%spg%d/" % (base_url, i)
                refer_url = base_url
                if i == 1:
                    pass;
                elif i == 2:
                    tmp_head['Referer'] = base_url
                else:
                    tmp_head['Referer'] = "%spg%d/" % (base_url, i-1)
                time_1 = SLEEP_TIME + uniform (0, 2);
                time.sleep (time_1)
                yield scrapy.Request (new_url, headers = tmp_head, callback = self.pageCallback)
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

                if hid in self.id_map:
                    continue
                self.id_map.append (hid)

                prices_vec = []
                dates_vec = []
                now = str(datetime.date.today())
                if hid not in self.old_data_map:
                    # new home
#                    print "new home: %s" % (hid)
                    new_item = NewItem ()
                    new_item['title'] = title
                    new_item['address'] = address
                    new_item['prices'] = [price]
                    new_item['dates'] = [now]
                    new_item['hid'] = hid
                    yield new_item
                    
                else:
                    prices_vec = self.old_data_map[hid][0]
                    dates_vec = self.old_data_map[hid][1]
                    del self.old_data_map[hid]
                    
                if len(prices_vec) != 0 and prices_vec[-1] == price:
                    # do not need add
                    pass
                else:
                    prices_vec.append (price)
                    dates_vec.append (now)

                home_item = HomeItem ()
                home_item['title'] = title
                home_item['address'] = address
                home_item['prices'] = prices_vec
                home_item['dates'] = dates_vec
                home_item['hid'] = hid
                yield home_item
                
        else:
            logging.error ("request page: %s failed %s", response.url, response.status);
