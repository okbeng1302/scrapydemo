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

class JobSpider(Spider):
	name = 'job'
	# start_urls = ['https://job.oschina.net/search?type=%E8%81%8C%E4%BD%8D%E6%90%9C%E7%B4%A2&key=web%E5%89%8D%E7%AB%AF&exp=0&edu=0&nat=1&city=%E5%85%A8%E5%9B%BD&p=1']
	keys = ['Java','Python','Hadoop','自然语言处理','搜索算法','全栈工程师','数据挖掘','后端其他','web前端',
			'HTML5','JavaScript','前端开发工程师','前端其他'
	]
	def start_requests(self):
		for k in self.keys:

			for i in range(1,12):
				url = 'https://job.oschina.net/search?type=职位搜索&key=%s&exp=0&edu=0&nat=1&city=全国&p=%s' %(k,i)
				yield Request(url=url,callback=self.parse)
	def parse(self,response):
		sel = Selector(response)

		list_jobdivs = sel.xpath('//div[@class="box clear layout"]')

		for div in list_jobdivs:
			job_url = div.xpath('./div[@class="flex-item-6 "]/div[@class="layout"]/div[@class="layout-left title"]/a/@href').extract()[0]
			company_url = div.xpath('./div[@class="flex-item-6 com-info"]/div[@class="layout clear"]/div[@class="layout-column"]/div[@class="layout"]/a/@href').extract()[0]
			yield Request(url=job_url,callback =self.parse_job)
			yield Request(url=company_url,callback =self.parse_company)


	def parse_company(self,response):
		sel = Selector(response)
		item = CompanyDetail()
		item['companyurl'] = response.url # 公司链接
		title = sel.xpath("//small/text()").extract()[0]
		item['companyname'] = title # 公司名称
		companydescs = sel.xpath("//div[@class='panel-body']")[0].re(r'<p>(.*?)</p>')
		companydesc = ''
		for c in companydescs:
			companydesc = companydesc + c
		companydesc = companydesc.replace("<br>","")
		item['companydesc'] = companydesc # 公司介绍
		# companyguimo = sel.xpath("//div[@class='col-xs-7']/ul[@class='lists text']/li")[1].xpath("./span[@class='size']/text()").extract()[0]
		# item['companyguimo'] = companyguimo # 公司规模
		# companyguanwang  = sel.xpath("//div[@class='col-xs-7']/ul[@class='lists text']/li")[2].xpath("./span[@class='page']/a/@href").extract()[0]
		# item['companyguanwang'] = companyguanwang
		# companyjieduan = sel.xpath("//div[@class='col-xs-7']/ul[@class='lists text']/li")[3].xpath("./span[@class='stage']").extract()[0]
		# item['companyjieduan'] = companyjieduan
		yield item
	def parse_job(self,response):
		# print response.url
		sel = Selector(response)
		item = JobDetail()
		item['joburl'] = response.url # 职位链接
		company = sel.xpath("//div[@class='col-xs-12']/h3[@class='text-left']/strong/a/@title").extract()[0]
		item['jobcompany'] = company # 公司名称
		title = sel.xpath("//h1/@title").extract()[0]
		item['jobcontent'] = title # 公司岗位
		jobmoney = sel.xpath("//div[@class='left']/div[@class='basic']/div[@class='clearfix row lh-md']/div[@class='col-xs-9']/div/b/text()").extract()[0]
		item['jobmoney'] = jobmoney # 工作薪资
		locations = sel.xpath("//div[@class='left']/div[@class='basic']/div[@class='clearfix row lh-md']/div[@class='col-xs-9']/div/a")
		jobneed = ''
		for l in locations:
			jobneed = jobneed + l.xpath("./text()").extract()[0].strip()+'/'
		item['jobneed'] = jobneed # 工作要求 包括地点 学历 经验 
		skillneed = ''
		skills = sel.xpath("//div[@class='left']/div[@class='basic']/div[@class='clearfix row lh-md']/div[@class='col-xs-9']/div/span[@id='ex-position-skills']/a")
		for s in skills:
			skillneed = skillneed + s.xpath("./text()").extract()[0].strip() + '/'
		skillneed = skillneed[:len(skillneed)-1]
		item['skillneed'] = skillneed # 技能要求
		pubtime = sel.xpath("//div[@class='left']/div[@class='basic']/p/text()").extract()[0]
		item['pubtime'] = pubtime # 发布时间

		jobdescs = sel.xpath("//div[@class='panel']/div[@class='panel-body']/div[@class='position-description']")[0].re(r'<p>(.*?)</p>')
		jobdesc = ''
		for j in jobdescs:
			jobdesc = jobdesc + j
		jobdesc = jobdesc.replace('<br>',"")
		item['jobdesc'] = jobdesc # 工作描述
		yield item

		# print company,title[0],response.url
