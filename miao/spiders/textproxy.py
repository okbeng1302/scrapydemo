# -*- coding:utf-8 -*-
# import requests

# try:
# 	requests.get('http://wenshu.court.gov.cn/', proxies={"http":"http://222.85.50.168:808"})
# except:
# 	print "failed"
# else:
# 	print "success"

# import re

# con = '链接:<a href="http://git.ghostscript.com/?p=ghostpdl.git;h=8210a2864372723b49c526e2b102fdc00c9c4699" target="_blank" rel="nofollow">http://git.ghostscript.com/?p=ghostpdl.git;h=8210a2864372723b49c526e2b102fdc00c9c4699</a>'

# aa = '.+?(?<=href=\").+?(?=\")'
# pattern = '(.+?)<a href=\"(.+?)\"'

# rel = re.findall(pattern,con)
# print rel
# for aa in rel[0]:
# 	print aa
# for i in range(1,50):
# 	url = 'http://www.cnnvd.org.cn/vulnerability/index/p/%s' %i
# 	print url
# a = []
# if len(a):
# 	print 'true'
# else:
# 	print 'false'

class Test():
	def __init__(self,name=None):
		if name is not None:
			self.name = name
			print self.name
		else:
			print 'name is null'
	def parse(self):
		print "ssss"

if __name__ == '__main__':
	a = 1
	test = Test(a)
	#test.parse()