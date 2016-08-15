#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests


reload(sys)
sys.setdefaultencoding('utf-8')
if(len(sys.argv)>=2):
    user_id = (int)(sys.argv[1])
else:
    #user_id = (int)(raw_input(u"请输入user_id: "))
    user_id = 1785051383

cookie = {"Cookie": ("_T_WM=ba9ca6cf0c242230b0b02cc2999f082c;"
                     "ALF=1473650538;"
                     "SCF=AgKXtrN1eQdopeXBBkOn_FlCMdn7iXFQsrKkhqWKEaLOxb2vQrmPaQkRv4mdSkrV_cjeZiiDjHdgWtbfCLkCWBI.;"
                     "SUB=_2A256tVYKDeTxGeRO6FAT8SfNzTuIHXVWVnpCrDV6PUNbktBeLUv2kW2YB5v06cuGST-jsCIj8PP3pXcE0A..;"
                     "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhdP4labCQQTUd1BBj3w4kL5JpX5KMhUgL.Foz7e0zEeK.pSoM2dJLoIpXLxKqL1-BL12-LxK-LB.zLB.2LxK-L1hMLB-9jIBtt;"
                     "SUHB=0XDkRf8qxsWNei;"
                     "SSOLoginState=1471227482;"
                     "H5_INDEX=1;"
                     "H5_INDEX_TITLE=%E6%9D%8E%E5%BB%BA%E5%87%AFli;"
                     "M_WEIBOCN_PARAMS=uicode%3D20000174")}
url = 'http://weibo.cn/u/%d?filter=1&page=1'%user_id
html = requests.get(url, cookies = cookie).content
print html
filepath = os.getcwd() + "/text"
fileHandle = open(filepath,'w')
fileHandle.write(html)

soup = BeautifulSoup(html, 'html5lib')

print "----selector----"
print soup

temp = soup.find_all('ctt')
print temp

#pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
pageNum = 5
print "PageNUM : %d"%pageNum

while True:
    pass

result = ""
urllist_set = set()
word_count = 1
image_count = 1


print u'爬虫准备就绪...'

for page in range(1,pageNum+1):

  #获取lxml页面
  url = 'http://weibo.cn/u/%d?filter=1&page=%d'%(user_id,page)
  lxml = requests.get(url, cookies = cookie).content

  #文字爬取
  selector = etree.HTML(lxml)
  content = selector.xpath('//span[@class="ctt"]')
  for each in content:
    text = each.xpath('string(.)')
    if word_count>=4:
      text = "%d :"%(word_count-3) +text+"\n\n"
    else :
      text = text+"\n\n"
    result = result + text
    word_count += 1

  #图片爬取
  soup = BeautifulSoup(lxml, "lxml")
  urllist = soup.find_all('a',href=re.compile(r'^http://weibo.cn/mblog/oripic',re.I))
  first = 0
  for imgurl in urllist:
    urllist_set.add(requests.get(imgurl['href'], cookies = cookie).url)
    image_count +=1

filepath = os.getcwd() + ("/%s"%user_id)
print filepath
fo = open(filepath, "wb")
fo.write(result)
word_path=os.getcwd()+'/%d'%user_id
print u'文字微博爬取完毕'

link = ""
filepath = os.getcwd() + ("/%s_imageurls"%user_id)
fo2 = open(filepath, "wb")
for eachlink in urllist_set:
  link = link + eachlink +"\n"
fo2.write(link)
print u'图片链接爬取完毕'

print u'原创微博爬取完毕，共%d条，保存路径%s'%(word_count-4,word_path)

