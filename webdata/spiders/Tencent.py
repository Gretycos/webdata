# -*- coding: utf-8 -*-
import scrapy


class TencentSpider(scrapy.Spider):
    name = 'Tencent'
    allowed_domains = ['v.qq.com']
    start_urls = ['http://v.qq.com/']

    def parse(self, response):
        pass
