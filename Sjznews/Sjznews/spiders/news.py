# -*- coding: utf-8 -*-
import scrapy
from Sjznews.items import SjznewsItem
import re
import time

class NewsSpider(scrapy.Spider):
    name = 'news'
    year = time.strftime("%Y")
    month = time.strftime("%m")
    day = time.strftime("%d")
    #allowed_domains = ['http://sjzrb.sjzdaily.com.cn/']
    str_url = 'http://sjzrb.sjzdaily.com.cn/html/' +year+'-'+month+ '/'+day +'/node_5.htm'#每天开始爬取的初始界面
    start_urls = [str_url]


    def parse(self, response):
        for herf in response.css('a::attr("href")').extract():
            next_herf = re.findall(r'node_\d*.htm.*', herf)
            for p in next_herf:
                m = re.search(r'node_\d*.htm', response.url)
                in_urls = response.url.rstrip(m.group(0)) + p.rstrip('\'>,')
                yield scrapy.Request(in_urls, callback=self.parse_2)

    def parse_2(self, response):
        for herf in response.css('a::attr("href")').extract():
            layout_herf = re.findall(r'content_\d*.htm.*', herf)
            for m in layout_herf:
                n = re.search(r'node_\d*.htm', response.url)
                url = response.url.rstrip(n.group(0)) + m.rstrip('\'>,')
                yield scrapy.Request(url, callback=self.parse_news)

    def parse_news(self, response):
        item = SjznewsItem()
        item['title'] = response.xpath('//strong/text()').extract()
        item['source'] = response.xpath('//tbody/tr/td/span/a/text()').extract()
        item['main'] = response.xpath('//tbody/tr/td/div//text()').extract()
        yield item

