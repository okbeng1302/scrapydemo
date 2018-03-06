# -*- coding:utf-8 -*-
import logging
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from miao.items import JobDetail,CompanyDetail
from hashlib import md5
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class XdfSpider(Spider):
	name = 'xdf'

	start_urls = ["http://www.xdf.cn/"]


	def parse(self,response):

		print response.body
		file = open('e:/hanhan/xdf.txt','wb')
		file.write(response.body)
		file.close()
