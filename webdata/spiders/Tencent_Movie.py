# -*- coding: utf-8 -*-
import random
import time

import demjson
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from webdata.items import MovieItem


class Tencent_MovieSpider(scrapy.Spider):
    name = 'Tencent_Movie'
    custom_settings = {
        'ITEM_PIPELINES': {
            'webdata.pipelines.MoviePipeline': 500
        }
    }
    allowed_domains = ['v.qq.com']
    start_urls = ['https://v.qq.com/channel/movie?listpage=1&channel=movie&sort=18&_all=1']
    driver = None
    page = 71  # 爬取页数

    def parse(self, response):
        """
        处理爬虫请求：
            从api中抽取出信息
        :param response:
        :return:
        """
        print("启动中...")
        self.driver_init()
        self.driver.get(response.url)
        time.sleep(2)
        print("跳转中...")
        for i in range(0,self.page):
            print("正在爬取第{}页...".format(i+1))
            real_url = 'https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&channel=movie&listpage=2&offset={}&pagesize=30&sort=18'.format(i*30)
            yield scrapy.Request(url=real_url, callback=self.myParse)
            if i != self.page-1:
                time.sleep(random.random()+1)
        self.driver.quit()

    def myParse(self, response):
        records = response.xpath('/html/body/div')
        for div in records:
            movie = MovieItem()
            id = div.xpath('./a/@data-float').extract_first()
            if id is None:
                continue
            # print(id)
            movie['_id'] = id
            movie['title'] = div.xpath('./a/@title').extract_first()
            movie['link'] = div.xpath('./a/@href').extract_first()
            movie['cover'] = ['https:{}'.format(div.xpath('./a/img[1]/@src').extract_first())]
            movie['play_count'] = self.parsePlayCount('{}次播放'.format(div.xpath('./div[2]/text()').extract_first()))
            movie['source'] = 'tencent'
            yield movie

    def parsePlayCount(self, count):
        """
        处理播放量：
            统一单位
        :param count:
        :return count:
        """
        if count[-4] == '亿':
            count = count.replace(count[0:-4], str(int(count[0:-4]) * 10000))
            count = count.replace(count[-4], '万')
        return count

    def driver_init(self):
        """
        浏览器初始化：
            设置浏览器、浏览器的选项
        """
        print("初始化中...")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument(
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36')
        self.driver = webdriver.Chrome(options=options)
