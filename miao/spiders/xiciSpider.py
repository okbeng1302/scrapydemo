import logging
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from miao.items import XiciItem
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class XiciSpider(Spider):
	name = 'xici'

	start_urls = ['http://www.xicidaili.com/']

	def parse(self,response):
		sel = Selector(response)
		table = sel.xpath('//table[@id="ip_list"]')[0]
		trs = table.xpath('//tr')[2:]
		

		for tr in trs:
			item = XiciItem()
			if len(tr.xpath('td[5]/text()').extract()) == 1:

				item['ip'] = tr.xpath('td[2]/text()').extract()[0]
				item['port'] = tr.xpath('td[3]/text()').extract()[0]
				item['address'] = tr.xpath('td[4]/text()').extract()
				item['isgaoni'] = tr.xpath('td[5]/text()').extract()[0]
				item['iptype'] = tr.xpath('td[6]/text()').extract()[0]
				item['time'] = tr.xpath('td[7]/text()').extract()[0]
				item['valid'] = tr.xpath('td[8]/text()').extract()[0]
				yield item
			