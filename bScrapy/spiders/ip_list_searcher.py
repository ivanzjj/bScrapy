#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import urllib
import zlib
from lxml import etree
from cookielib import CookieJar
from bs4 import BeautifulSoup

def getxpath(html):
    return etree.HTML(html)

cj = CookieJar()
proxy = urllib2.ProxyHandler({'https': '183.153.6.169:808', 'http': '183.153.6.169:808'})
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), proxy)

url = "http://www.xicidaili.com/wn/"

headers = {
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "DNT": "1",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ru;q=0.2,es;q=0.2",
}
request = urllib2.Request (url, headers= headers)
response = opener.open (request)
zip_data = response.read ()
unzip_data = zlib.decompress(zip_data, 16+zlib.MAX_WBITS)

soup = BeautifulSoup(unzip_data,'lxml')
mydivs = soup.findAll("tr", { "class" : "odd" })
for div in mydivs:
    ip = div.find_all ('td')[1].contents[0]
    port = div.find_all ('td')[2].contents[0]
    print ip, port

'''
body = getxpath (unzip_data)
ip_lists = body.xpath ('//body[1]/div[1]/div[2]/table[1]/tbody')
#ip_lists = body.xpath ('//body[1]/div[1]/div[2]/table[1]/tbody[1]')
print type(ip_lists), len(ip_lists)
print ip_lists
for ip_tr in ip_lists:
    ip = ip_tr.xpath ('tr[@class="odd"]/td[2]//text ()').extract_first ()
    print type(ip), ip
'''

