import logging
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from miao.items import ChinaItem
import re
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ChinaSpider(Spider):
	name = 'china'

	start_urls = ['http://hotel.qunar.com/']

	# def start_requests(self):

	# 	for i in range(1,2):
	# 		url = 'http://www.cnnvd.org.cn/vulnerability/index/p/%s' %i

	# 		yield Request(url=url,callback=self.parse)

	def parse(self,response):
		sel = Selector(response)
		print response.url
		f = open("E:/hanhan/china2.txt","wb")
		f.write(response.body)
		f.close()

	# 	links = sel.xpath(".//div/div[@class='container']//table[@class='qtld_details sortable']/tbody/tr/td[4]/a")
	# 	for link in links:
	# 		sel_url =  link.xpath('.//@href').extract()[0]
	# 		#print link.xpath('.//@title').extract()[0]
	# 		url = 'http://www.cnnvd.org.cn' + sel_url
	# 		#print url
	# 		yield Request(url=url,callback=self.parse_content)
	# def parse_content(self,response):

	# 	print response.url
	# 	item = ChinaItem()
	# 	item['url'] = response.url
	# 	name = response.xpath(".//table[@id='__01']/tr/td/table/tr/td/div/table/tr[1]/td[2]/text()").extract()
	# 	if len(name):
	# 		name = name[0]
	# 	else:
	# 		name = ''
	# 	item['name'] = name
	# 	ghosttype = response.xpath(".//table[@id='__01']/tr/td/table/tr/td/div/table/tr[6]/td[2]/a/text()").extract()
	# 	if len(ghosttype):
	# 		ghosttype = ghosttype[0]
	# 	else:
	# 		ghosttype = ''
	# 	item['ghosttype'] = ghosttype
	# 	descriptions = response.xpath(".//table[@id='__01']/tr/td/table/tr[2]/td/div/p/text()").extract()
	# 	desc = ''
	# 	for description in descriptions:
	# 		desc = desc + description
	# 	item['description'] = desc
	# 	pub_content = response.xpath(".//table[@id='__01']/tr/td/table/tr[3]/td/div/p/text()").extract()
	# 	if len(pub_content):
	# 		pub_content = pub_content[0]
	# 	else:
	# 		pub_content = ''
	# 	pub_link = response.xpath(".//table[@id='__01']/tr/td/table/tr[3]/td/div/p/a/text()").extract()
	# 	if len(pub_link):
	# 		pub_link = pub_link[0]
	# 	else:
	# 		pub_link = ''
	# 	item['publication'] = pub_content + pub_link

	# 	ref = response.xpath(".//table[@id='__01']/tr/td/table/tr[4]/td/div/table/tr/td/p")[0].re(r'(.*?)<br>(.*?)<br>')
	# 	arr_ref = []

	# 	for r in ref:
	# 		if r.strip() =='':
	# 			pass
	# 		else:
	# 			arr_ref.append(r)
	# 	reference = ''
	# 	ref_link = ''
	# 	pattern = '(.+?)<a href=\"(.+?)\"' 
	# 	for index in range(len(arr_ref)):
	# 		if (index % 2) == 0:
	# 			reference = reference + arr_ref[index]
	# 			#print reference
	# 		else:
	# 			refs = re.findall(pattern,arr_ref[index])[0]
	# 			for s in refs:
	# 				ref_link = ref_link + s
	# 			reference = reference + ref_link
	# 	item['reference'] = reference

	# 	yield item

