# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item


class MiaoItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    link = Field()
    desc = Field()
    content = Field()
class BaiduItem(Item):
	title = Field()
	url = Field()
	content = Field()

class XiciItem(Item):
	ip = Field()
	port = Field()
	address = Field()
	isgaoni = Field()
	iptype = Field()
	time = Field()
	valid = Field()

class ChinaItem(Item):
	name = Field()
	ghosttype = Field()
	description = Field()
	publication = Field()
	reference = Field()
	url = Field()

# 抓取 oschina 招聘信息
class JobItem(Item):
	joburl = Field() # 工作链接
	jobcontent = Field() # 工作岗位
	joblocation = Field() # 工作地点
	skillreq = Field() # 技能要求
	time = Field() # 发布时间
	url = Field() # 招聘链接
	companyurl = Field() # 公司详情链接

class JobDetail(Item):
	joburl = Field() # 工作链接
	jobcompany = Field() # 公司名称
	jobcontent = Field() # 工作岗位
	jobmoney = Field() # 工作薪资
	jobneed = Field() # 工作要求
	skillneed = Field() # 技能要求
	pubtime = Field() # 发布时间
	jobdesc = Field() # 职位描述

class CompanyDetail(Item):
	companyurl = Field() # 公司链接
	companyname = Field() # 公司名称
	companydesc = Field() # 公司介绍
	# companyguimo = Field() # 公司规模
	# companyguanwang = Field() # 公司官网
	# companyjieduan = Field() # 公司阶段


