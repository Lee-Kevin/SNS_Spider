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
import time
import Queue

reload(sys)
sys.setdefaultencoding('utf-8')
if(len(sys.argv)>=2):
    user_id = (int)(sys.argv[1])
else:
    #user_id = (int)(raw_input(u"请输入user_id: "))
    user_id = 1785051383

cookie = {"Cookie": ("_T_WM=ba9ca6cf0c242230b0b02cc2999f082c;"
                     "ALF=1473925225;"
                     "SCF=AgKXtrN1eQdopeXBBkOn_FlCMdn7iXFQsrKkhqWKEaLOvsdX199Xm3L55pzbpM5yXaQJV6IXGnbUlpqJDt6W-vY.;"
                     "SUB=_2A256t8_3DeTxGeRO6FAT8SfNzTuIHXVWW9G_rDV6PUNbktBeLVT4kW1NCCUtKRMSaGPpnjbluGsLwNKCcA..;"
                     "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhdP4labCQQTUd1BBj3w4kL5JpX5KMhUgL.Foz7e0zEeK.pSoM2dJLoIpXLxKqL1-BL12-LxK-LB.zLB.2LxK-L1hMLB-9jIBtt;"
                     "SUHB=0C1D3u25gu-YLZ;"
                     "SSOLoginState=1471397800;"
                     "M_WEIBOCN_PARAMS=uicode%3D20000174")}

url = 'http://weibo.cn/u/%d?filter=1&page=1'%user_id

soup = BeautifulSoup(requests.get(url, cookies = cookie).content, 'html5lib')

print "------------------------------"
new_message = ''
last_message = ''
spans = soup.find_all(re.compile("span"),limit = 12)
print spans[2].text[0:17]
new_message = spans[9].text + spans[8].text

print new_message
last_message = new_message
new_message1 = spans[11].text + " :" + spans[10].text
print new_message1
filepath = os.getcwd() + "/message"
filepath1 = os.getcwd() + "/printFlag"

fileHandle = open(filepath, "wb")
fileHandle.write(new_message + "\n")

fileHandle.write(new_message1 + "\n")
fileHandle.close()

fileHandle = open(filepath1,"wb")
fileHandle.write("1")
fileHandle.close()

while True:
    try:
        soup = BeautifulSoup(requests.get(url, cookies=cookie).content, 'html5lib')
        spans = soup.find_all(re.compile("span"), limit=12)
        new_message = spans[9].text + spans[8].text
        if last_message == new_message:
            print "----The Result is Different----\n"
        else :
            fileHandle = open(filepath, "wb")
            fileHandle.write(new_message + "\n")
            fileHandle.close()
            fileHandle = open(filepath1,"wb")
            fileHandle.write("1")
            fileHandle.close()
            last_message = new_message

        time.sleep(6)
    except Exception,e:
        print e

