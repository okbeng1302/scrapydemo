# -*- coding:utf-8 -*-
import logging
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from miao.items import BaiduItem
from hashlib import md5
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class BaiduSpider(Spider):
	name='baidu'
	start_urls = ['http://finance.sina.com.cn/']
	allowed_domains = ['finance.sina.com.cn']
	# def __init__(self):
		# self.f = open('E:/hanhan/datas.txt','a')

	def parse(self,response):
		sel = Selector(response)
		# # charset = response.headers['Content-Type']
		# print charset
		re_script = re.compile('<script[^>]*>[\s\S]*?<\/script>',re.I)
		re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)
		del_label = re.compile(r'<[^>]+>',re.S)
		body = response.body
		if not isinstance(body,unicode):
			try:
				body.decode('utf-8')
			except UnicodeDecodeError:
				body.decode('gbk','ignore')
		content_del = re_script.sub('',body)
		content_del = re_style.sub("",content_del)
		content_del = del_label.sub("",content_del)
		content_del = content_del.replace('\t','').replace(' ','')
		content_del = content_del.split('\n')
		content = ''
		for c in content_del:
			if c:
				if len(c) != 1:
					content = content + c.strip() + '\n'
		link_title = sel.xpath('//title/text()').extract_first(default = "").strip()
		print response.url,link_title
		links = sel.xpath('//a[contains(@href,"//")]')
		for link in links:
			weburl = link.xpath('./@href').extract()[0]
			utf8_url = weburl.encode('utf-8')
            # print utf8_url
			postfix = re.compile(r'.+\.((jpg)|(ico)|(rar)|(zip)|(doc)|(ppt)|(xls)|(css)|(exe)|(pdf))x?$')
			prefix = re.compile(r'^((javascript:)|(openapi)).+')
			if postfix.match(utf8_url):
				continue
			if prefix.match(utf8_url):
				continue
			if not utf8_url.startswith('http'):
				if not utf8_url.startswith('www'):
					weburl = response.url + '/' + weburl
				else:
					weburl = self.geturlproto(response.url) + self.gethostname(response.url) + '/' + weburl
			weburl = re.sub(r'/\.\./\.\./', r'/', weburl)
			weburl = re.sub(r'/\.\./', r'/', weburl)
			# logging.log(logging.WARNING, "link内容为：" + str(weburl))
			yield Request(url=weburl, callback=self.parse)
		# clear1 = re.compile('<\s*script type=[^>]*>[^<]*<\s*/\s*script\s*>')
		# content = clear1.sub("",content)
		filename = self._get_linkmd5id(response.url)
		# self.f.write(content)
		output = open("D:/hanhan/pages/"+str(filename)+".txt","wb")
		output.write(content)
		output.close()
		

	def spider_closed(self, spider, reason):
		self.f.close()

	def _get_linkmd5id(self, url):
		# url进行md5处理，为避免重复采集设计
		return md5(url).hexdigest()



