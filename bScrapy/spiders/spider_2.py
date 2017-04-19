#!/usr/bin/env python
# -*- coding:utf-8 -*-

import scrapy
import urllib
import logging
from scrapy.spiders import CrawlSpider, Rule

START_URL = "http://bj.lianjia.com/ershoufang/"

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
    def start_requests(self):
        logging.info ("start crawl LianJian site.");
        tmp_head = COMMON_HEADER;
        tmp_head["Host"] = "http://bj.lianjia.com/ershoufang/"
        yield scrapy.Request (START_URL, headers = tmp_head, callback = self.homePageCallback)

    def homePageCallback(self, response):
        if response.status is 200:
            logging.info ("LianJia HomePage load success.");
            print response.body
            districts = response.xpath ("/html/body/div[3]/div[1]/dl[2]/dd/div[1]/div/a")
            tmp_head = COMMON_HEADER;
            tmp_head["Host"] = "bj.lianjia.com"
            for district in districts:
                district_name = district.xpath("text()").extract_first ()
                district_url = district.xpath("@href").extract_first ()
                new_url = "http://bj.lianjia.com%s" % (district_url)
                print "found new url: %s" % (new_url)
                yield scrapy.Request (new_url, headers = tmp_head, callback = self.workCallback);
        else:
            logging.error ("LianJia HomePage load failed %s" % (response.status))

    def workCallback(self, response):
        if response.status is 200:

            next_page = response.xpath("/html/body/div[4]/div[1]/div[7]/div[2]/div[1]/a[4]")
            print next_page, type (next_page)
            
            homes = response.xpath("/html/body/div[4]/div[1]/ul/li");
            for home in homes:
                title = home.xpath ("div[1]/div[1]/a//text()").extract_first ()
                address = home.xpath ("div[1]/div[2]/div/a//text()").extract_first ()
                price = home.xpath ("div[1]/div[6]/div[1]/span//text()").extract_first ()
        else:
            logging.error ("failed");
