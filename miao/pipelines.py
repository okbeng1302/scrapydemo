# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from hashlib import md5
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column,String,create_engine, DateTime, Integer, Text, INT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey,Table
from sqlalchemy.orm import relationship,backref
from datetime import datetime
from items import JobDetail,CompanyDetail
from sqlalchemy.dialects.mysql import LONGTEXT
engine = create_engine('mysql+mysqldb://root:1234@127.0.0.1:3306/iproxypool?charset=utf8')
DBSession = sessionmaker(bind=engine)
Base = declarative_base()
from scrapy.conf import settings
# import pymongo
import pymongo

class MongoDBPipeline(object):
	def __init__(self):
		# 创建连接
		client = pymongo.MongoClient('localhost',27017)
		# 连接数据库
		db = client.xiaobai
		# 连接集合
		self.collection_job = db.job
		self.collection_company = db.company
	def process_item(self,item,spider):
		valid = True
		for data in item:
			if not data:
				valid = False
				raise DropItem("Missing {0}!".format(data))
		if valid:
			if isinstance(item,JobDetail):
				self.collection_job.insert(dict(item))
				print ("Job is adding to MongoDB!")
			else:
				self.collection_company.insert(dict(item))
				print ("Company is adding to MongoDB!")
		return item


class MiaoPipeline(object):
    def process_item(self, item, spider):
        return item
class BaiduPipeline(object):
    def __init__(self):
    	self.file = codecs.open('baidu_url.json','wb',encoding='utf-8')

    def process_item(self, item, spider):
    	print item
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.decode('unicode_escape'))
        return item

class Iptable(Base):
	__tablename__ = 'iptable'

	id = Column(Integer,primary_key = True,autoincrement = True)
	ip = Column(String(255))
	port = Column(String(255))
	address = Column(String(255))
	isgaoni = Column(String(255))
	iptype = Column(String(255))
	time = Column(String(255))
	valid = Column(String(255))

class China(Base):
	__tablename__ = 'china'

	linkmd5id = Column(Integer,primary_key = True)
	name = Column(String(255))
	ghosttype = Column(String(255))
	description = Column(LONGTEXT)
	publication = Column(LONGTEXT)
	reference = Column(LONGTEXT)
	url = Column(String(255))

class Job(Base):
	__tablename__ = 'job'

	id = Column(Integer,primary_key = True,autoincrement = True)
	joburl = Column(String(255))
	jobcompany = Column(String(255))
	jobcontent = Column(String(255))
	jobmoney = Column(String(255))
	jobneed = Column(String(255))
	skillneed = Column(String(255))
	pubtime = Column(String(255))
	jobdesc = Column(LONGTEXT)
class Company(Base):
	__tablename__ = "company"

	id = Column(Integer,primary_key = True,autoincrement = True)
	companyurl = Column(String(255))
	companyname = Column(String(255))
	companydesc = Column(LONGTEXT)
	# companyguimo = Column(String(255))
	# companyguanwang = Column(String(255))
	# companyjieduan = Column(String(255))



class ChinaPipeline(object):
	def open_spider(self,spider):
		self.session = DBSession()
	def process_item(self,item,spider):

		linkmd5id = self._get_linkmd5id(item)
		isurl = self.session.query(China).filter(China.linkmd5id==linkmd5id).all()
		if isurl:
			self.session.query(China).filter(China.linkmd5id==linkmd5id).update({China.url:item['url']})
			self.session.query(China).filter(China.linkmd5id==linkmd5id).update({China.name:item['name']})
			self.session.query(China).filter(China.linkmd5id==linkmd5id).update({China.ghosttype:item['ghosttype']})
			self.session.query(China).filter(China.linkmd5id==linkmd5id).update({China.description:item['description']})
			self.session.query(China).filter(China.linkmd5id==linkmd5id).update({China.publication:item['publication']})
			self.session.query(China).filter(China.linkmd5id==linkmd5id).update({China.reference:item['reference']})
			self.session.commit()
		else:
			ch = China(linkmd5id=linkmd5id,
						name=item['name'],
						ghosttype=item['ghosttype'],
						description=item['description'],
						publication=item['publication'],
						reference=item['reference'],
						url=item['url']
				)
			self.session.add(ch)
			self.session.commit()

	def close_spider(self,spider):
		self.session.close()

	def _get_linkmd5id(self,item):
		return md5(item['url']).hexdigest()

class JobPipeline(object):

	def open_spider(self,spider):
		self.session = DBSession()
	def process_item(self,item,spider):
		if isinstance(item,JobDetail):
			isexists = self.session.query(Job).filter(Job.joburl == item['joburl']).all()
			if isexists:
				self.session.query(Job).filter(Job.joburl==item['joburl']).update({Job.joburl:item['joburl']})
				self.session.query(Job).filter(Job.jobcompany==item['jobcompany']).update({Job.jobcompany:item['jobcompany']})
				self.session.query(Job).filter(Job.jobcontent==item['jobcontent']).update({Job.jobcontent:item['jobcontent']})
				self.session.query(Job).filter(Job.jobmoney==item['jobmoney']).update({Job.jobmoney:item['jobmoney']})
				self.session.query(Job).filter(Job.jobneed==item['jobneed']).update({Job.jobneed:item['jobneed']})
				self.session.query(Job).filter(Job.skillneed==item['skillneed']).update({Job.skillneed:item['skillneed']})
				self.session.query(Job).filter(Job.pubtime==item['pubtime']).update({Job.pubtime:item['pubtime']})
				self.session.query(Job).filter(Job.jobdesc==item['jobdesc']).update({Job.jobdesc:item['jobdesc']})
				self.session.commit()
			else:
				jobs = Job(joburl=item['joburl'],
					jobcompany=item['jobcompany'],
					jobcontent=item['jobcontent'],
					jobmoney=item['jobmoney'],
					jobneed=item['jobneed'],
					skillneed=item['skillneed'],
					pubtime=item['pubtime'],
					jobdesc=item['jobdesc'])
				self.session.add(jobs)
				self.session.commit()
		else:
			isexists = self.session.query(Company).filter(Company.companyname == item['companyname']).all()

			if isexists:
				self.session.query(Company).filter(Company.companyurl==item['companyurl']).update({Company.companyurl:item['companyurl']})
				self.session.query(Company).filter(Company.companyname==item['companyname']).update({Company.companyname:item['companyname']})
				self.session.query(Company).filter(Company.companydesc==item['companydesc']).update({Company.companydesc:item['companydesc']})
				# self.session.query(Company).filter(Company.companyguimo==item['companyguimo']).update({Company.companyguimo:item['companyguimo']})
				# self.session.query(Company).filter(Company.companyguanwang==item['companyguanwang']).update({Company.companyguanwang:item['companyguanwang']})
				# self.session.query(Company).filter(Company.companyjieduan==item['companyjieduan']).update({Company.companyjieduan:item['companyjieduan']})
				self.session.commit()
			else:
				companys = Company(companyurl=item['companyurl'],
					companyname=item['companyname'],
					companydesc=item['companydesc'])
					# companyguimo=item['companyguimo'],
					# companyguanwang=item['companyguanwang'],
					# companyjieduan=item['companyjieduan'])
				self.session.add(companys)
				self.session.commit()

class XiciPipeline(object):
	def open_spider(self,spider):
		self.session = DBSession()
	def process_item(self,item,spider):

		isexists = self.session.query(Iptable).filter(Iptable.ip == item['ip']).all()

		if isexists:
			self.session.query(Iptable).filter(Iptable.ip==item['ip']).update({Iptable.ip:item['ip']})
			self.session.query(Iptable).filter(Iptable.ip==item['port']).update({Iptable.ip:item['port']})
			self.session.query(Iptable).filter(Iptable.ip==item['address']).update({Iptable.ip:item['address']})
			self.session.query(Iptable).filter(Iptable.ip==item['isgaoni']).update({Iptable.ip:item['isgaoni']})
			self.session.query(Iptable).filter(Iptable.ip==item['iptype']).update({Iptable.ip:item['iptype']})
			self.session.query(Iptable).filter(Iptable.ip==item['time']).update({Iptable.ip:item['time']})
			self.session.query(Iptable).filter(Iptable.ip==item['valid']).update({Iptable.ip:item['valid']})
			self.session.commit()
		else:
			ips = Iptable(ip=item['ip'],
				port=item['port'],
				address=item['address'],
				isgaoni=item['isgaoni'],
				iptype=item['iptype'],
				time=item['time'],
				valid=item['valid'])
			self.session.add(ips)
			self.session.commit()
		
		#	self.session.close()
	def close_spider(self,spider):
		#self.session.close()
		pass