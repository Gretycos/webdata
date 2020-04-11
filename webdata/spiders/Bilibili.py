# -*- coding: utf-8 -*-
import json
import random
import time

import demjson
import scrapy

# from bilibili.spiders import BiliLogin
from selenium import webdriver

from webdata.items import WebdataItem

ID = '18376682801'
PWD = '12123312'

class BilibiliSpider(scrapy.Spider):
    name = 'Bilibili' # 爬虫的唯一标识符
    allowed_domains = ['www.bilibili.com','api.bilibili.com'] # 设置不过滤的域名
    start_urls = ['http://www.bilibili.com/']
    # loginManager = BiliLogin.BilibiliLogin(url=None,username=None,password=None) # 登录器
    driver = None
    page = 151 # 爬取页数

    # def parse(self, response):
    #     self.loginManager = BiliLogin.BilibiliLogin(url=response.url, username=ID, password=PWD)
    #     if not self.loginManager.biliLogin():
    #         pass
    #     self.driver.find_element_by_xpath('//*[@id="primaryChannelMenu"]/span[2]/div/a').click()
    #     time.sleep(1)
    #     self.driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[1]/div[1]/div[2]/a[3]').click()
    #     time.sleep(1)
    #     for i in range(1, self.page):
    #         real_url = 'https://api.bilibili.com/pgc/season/index/result?st=1&order=2&season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&sort=0&page={}&season_type=1&pagesize=20&type=1'.format(
    #             i)
    #         yield scrapy.Request(url=real_url, callback=self.myParse)
    #         time.sleep(5)

    def parse(self, response):
        self.driver_init()
        self.driver.get(response.url)
        print("跳转中...")
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="primaryChannelMenu"]/span[2]/div/a').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[1]/div[1]/div[2]/a[3]').click()
        time.sleep(1)
        for i in range(1,self.page):
            real_url = 'https://api.bilibili.com/pgc/season/index/result?st=1&order=2&season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&sort=0&page={}&season_type=1&pagesize=20&type=1'.format(i)
            print("正在爬取第{}页...".format(i))
            yield scrapy.Request(url=real_url,callback=self.myParse)
            time.sleep(random.randint(1,3)+random.random())
        self.driver.quit()

    def myParse(self, response):
        content = demjson.decode(response.body)
        data = content['data']['list']
        # print(data)
        anime = WebdataItem()
        for item in data:
            anime['_id'] = item['media_id']  # key
            anime['title'] = item['title']  # 名称
            anime['link'] = item['link']  # 链接
            anime['process'] = item['index_show']  # 更新进度
            anime['cover'] = item['cover']  # 封面
            anime['play_count'] = item['order']  # 播放量
            anime['source'] = 'bilibili'
            yield anime

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

