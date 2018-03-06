# coding:utf-8
import logging
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders.crawl import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
import re
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class ItjzSpider(CrawlSpider):
    name = 'itjz'
    allowed_domains = ['xueqiu.com']
    start_urls = ['https://xueqiu.com/5296621426/95168957']

    def parse(self, response):
        print response.url
        print response.headers

        ret = re.findall(r'window\.SNOWMAN_STATUS = (.*?);', response.body, re.S)
        print(ret[0].encode('gbk'))
        # for info in info_list:
        #     print(info)
        #     title = info.xpath('//span[contains(@class,"long")]/a')
        #     print(title)
        #     url = info.xpath('//span[contains(@class,"scopes")]/a[@target="_blank"]/@href').extract()
        #     print(url)
