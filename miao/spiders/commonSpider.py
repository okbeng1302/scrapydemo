# -*- coding:utf-8 -*-
import logging
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spidermiddlewares.httperror import HttpError
from miao.items import MiaoItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import FormRequest
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError,TCPTimedOutError
import re
import urllib2
import json
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class commonSpider(Spider):
	name = 'miao'
	start_urls=[
		# 'http://www.ifeng.com/',
		'http://www.sina.com.cn'
	]
	#allowed_domians = ['www.zhihu.com']
	custom_settings = {
	 		'DEPTH_LIMIT':'%s' % '9',
	 		'DOWNLOAD_DELAY' : '3'
	}
	def __init__(self):
		print 'starting...'
	 	self.allowed_domians = ['sina.com']
	def start_requests(self):
		for url in self.start_urls:
			yield Request(url,callback=self.parse,errback=self.errback_httpbin)
	# def parse(self,response):
	# 	sel = Selector(response)
	# 	refer_websites = sel.xpath('//a[contains(@href,"//")]/@href').extract()
		
	# 	for weburl in refer_websites:
	# 		# print website_url +'\n'
	# 		utf8_url = weburl.encode('utf-8')
	# 		print utf8_url
	# 		postfix = re.compile(r'.+\.((jpg)|(ico)|(rar)|(zip)|(doc)|(ppt)|(xls)|(css)|(exe)|(pdf))x?$')
	# 		prefix = re.compile(r'^((javascript:)|(openapi)).+')

	# 		if postfix.match(utf8_url):
	# 			continue
	# 		if prefix.match(utf8_url):
	# 			continue
	# 		if not utf8_url.startswith('http://'):
	# 			weburl = 'http://'+self.gethostname(response.url)+'/'+weburl

	# 		weburl = re.sub(r'/\.\./\.\./',r'/',weburl)
	# 		weburl = re.sub(r'/\.\./',r'/',weburl)
	# 		yield Request(url = weburl,callback=self.parse)
	# 	print len(refer_websites)

	# def gethostname(self,res_url):
	# 	proto, rest = urllib2.splittype(res_url)
	# 	host ,rest = urllib2.splithost(rest)
	# 	return host

# ----------关键字 获取 url---------
	def parse(self,response):
		sel = Selector(response)
		links = sel.xpath('//a[contains(@href,"//")]')
		for link in links:
			is_link_text = link.xpath('.//text()').extract_first(default = "").strip() 

			if not is_link_text.strip():
				link_text = link.xpath('.//span/text()').extract_first(default = "").strip() 
				#logging.log(logging.WARNING,"span内容为：" + str(link_text))
			# 	link_text = link_span.xpath('.tetx()').extract_first(default = "").strip() 
			# 	logging.log(logging.WARNING,"span_text内容为：" + str(link_span))
			else:
				link_text = is_link_text
				#logging.log(logging.WARNING,"link内容为：" + str(link_text))
			#print link_text
			# except:
			# 	link_text = link.xpath('.span/text()').extract()[1]
			# print type(link_text)
			key_word = u'股票'
			# if isinstance(key_word,unicode):
			# 	print 'key_word 是 Unicode类型'
			# if isinstance(link_text,unicode):
			# 	print 'link_text 是 Unicode类型'
			if link_text.find(key_word) != -1:
			 	weburl = link.xpath('./@href').extract()[0]
			 	print weburl
			 	utf8_url= weburl.encode('utf-8')
			 	postfix = re.compile(r'.+\.((jpg)|(ico)|(rar)|(zip)|(doc)|(ppt)|(xls)|(css)|(exe)|(pdf))x?$')
			 	prefix = re.compile(r'^((javascript:)|(openapi)).+')
			 	if postfix.match(utf8_url):
			 		continue
			 	if prefix.match(utf8_url):
			 		continue
			 	if not utf8_url.startswith('http://'):
			 		weburl = 'http://'+self.gethostname(response.url)+'/'+ weburl
			 	weburl = re.sub(r'/\.\./\.\./',r'/',weburl)
			 	weburl = re.sub(r'/\.\./',r'/',weburl)
			 	# print type(weburl)
			 	print weburl
			 	logging.log(logging.WARNING,"link内容为：" + str(weburl))
				yield Request(url=weburl,callback=self.parse)
		print len(links)

	def gethostname(self,res_url):
		proto, rest = urllib2.splittype(res_url)
		host ,rest = urllib2.splithost(rest)
		return host
		# for link_con in links_con:
		# 	print link_con
		# 	s
	def errback_httpbin(self, failure):
		# log all failures
		self.logger.error(repr(failure))
		# in case you want to do something special for some errors,
		# you may need the failure's type:
		if failure.check(HttpError):
		# these exceptions come from HttpError spider middleware
		# you can get the non-200 response
			response = failure.value.response
			self.logger.error('HttpError on %s', response.url)
		elif failure.check(DNSLookupError):
		# this is the original request
			request = failure.request
			self.logger.error('DNSLookupError on %s', request.url)
		elif failure.check(TimeoutError, TCPTimedOutError):
			request = failure.request
			self.logger.error('TimeoutError on %s', request.url)
#------模拟登录测试----------------
	# def start_requests(self):
	# 	return [Request('http://www.zhihu.com/#signin',errback=self.errback_httpbin,callback=self.login)]
	# def login(self,response):
	# 	print '##############login test##################'
	# 	sel = Selector(response)
	# 	_xsrf = sel.xpath('.//div[contains(@class,"view view-signin")]/form[contains(@method,"POST")]/input/@value').extract()
	# 	print _xsrf
	# 	return [FormRequest(
	# 		url = 'http://www.zhihu.com/#signin',
	# 		formdata={
	# 			'_xsrf':_xsrf,
	# 			'account':'18310381978',
	# 			'password':'guang1302',
	# 		},
	# 		callback=self.check_login,
	# 		)]


	# def check_login(self,response):
	# 	print response.url
	# 	print response.body
	# 	yield Request(
	# 		'http://www.zhihu.com',
	# 		callback = self.page_content,
	# 		dont_filter=True,
	# 			)
	# def page_content(self,response):
	# 	print response.body
	# 	with open('first_page.html',wb) as f:
	# 		f.write(response.body)
	# 	print 'done'


	# def errback_httpbin(self,failure):
	# 	print 'sssssssssss'
	# 	print failure
	# def parse(self,response):
	# 	print response.url
	# 	print response.body


	#allowed_domians = ['sina.com']
	#depth_limit = 1
	


	



# 正则获取 rules

	# rules = (Rule(LxmlLinkExtractor(allow=(),deny_domains=('club.baby.sina.com.cn','licaishi.sina.com.cn','db.auto.sina.com.cn')),callback = 'parse_obj',follow = True),)

	# def parse_start_url(self,response):
	# 	print response.url
	# 	yield Request(url=response.url,callback=parse_obj)
	# def parse_obj(self,response):
	# 	#print response.url
	# 	sel = Selector(response)
	# 	title = sel.xpath('//title/text()').extract()[0]
	# 	#print title
	# 	#for link in LxmlLinkExtractor(allow=(),deny_domains=('sina.com','blog.sina.com')).extract_links(response):
			




	