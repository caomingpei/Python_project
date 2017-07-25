#执行本文件 os.system直接执行命令

import os
import time

while True:
    rootfile = os.getcwd()
    os.system("scrapy crawl news")
    os.chdir('dataanalysis')
    os.system("python DA.py")
    time.sleep(86400)  #每隔一天运行一次 24*60*60=86400s