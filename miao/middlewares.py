# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.support import ui
from scrapy.http import HtmlResponse
import time
import re
agents = [
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
        'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)']
class ProxyMiddleware(object):
    def process_request(self,request,spider):
        request.meta['proxy'] = 'http://222.85.50.168:808'




class JavaScriptMiddleware(object):
    def process_request(self,request,spider):
        # pattern = re.compile('http://www.cnnvd.org.cn/vulnerability/index/p')
        # search_result = re.search(pattern,request.url)
        # if search_result:
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        agent = (random.choice(agents))
        dcap["phantomjs.page.settings.userAgent"] = (agent)#随机调用消UA
        # dcap["phantomjs.page.settings.loadImages"] = False#不加载图片
        print agent
        print "Phantomjs is starting"
        driver = webdriver.PhantomJS(desired_capabilities=dcap)

        # driver = webdriver.PhantomJS()
        wait = ui.WebDriverWait(driver, 15) 
        driver.set_window_size(1000, 10000)
        driver.get(request.url)
        # js1 = "var q=document.documentElement.scrollTop=5000"
        # driver.execute_script(js1)
        time.sleep(3)
        body = driver.page_source
        print "PhantomJS is visiting "+ request.url
        driver.close()
        driver.quit()
        return HtmlResponse(request.url, body=body, encoding='utf-8', request=request)
        # else:
        #     return
