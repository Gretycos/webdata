# -*- coding: utf-8 -*-
import json
import random
import time

import demjson
import scrapy

# from bilibili.spiders import BiliLogin
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from webdata.items import AnimeItem

ID = ''
PWD = ''

class BilibiliSpider(scrapy.Spider):
    name = 'Bilibili_Anime' # 爬虫的唯一标识符
    custom_settings = {
        'ITEM_PIPELINES':{
            'webdata.pipelines.AnimePipeline':400
        }
    }
    allowed_domains = ['www.bilibili.com'] # 设置不过滤的域名
    start_urls = ['https://www.bilibili.com/anime/index/#season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=1&st=1&sort=0&page=1']
    # loginManager = BiliLogin.BilibiliLogin(url=None,username=None,password=None) # 登录器
    driver = None
    page = 150 # 爬取页数

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
        """
        处理爬虫请求：
            使用selenium模拟浏览器点击、翻页，从结构中抽取出信息
        :param response:
        :return anime:
        """
        print("启动中...")
        self.driver_init()
        self.driver.get(response.url)
        time.sleep(5)
        print("跳转中...")
        self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/ul[1]/li[4]/span').click()
        time.sleep(5)
        for i in range(1,self.page+1):
            # real_url = 'https://api.bilibili.com/pgc/season/index/result?st=1&order=2&season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&sort=0&page={}&season_type=1&pagesize=20&type=1'.format(i)
            # yield scrapy.Request(url=real_url,callback=self.myParse)
            print("正在爬取第{}页...".format(i))
            self.scroll() # 滚动加载
            ul=self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/ul[2]')
            records = ul.find_elements_by_tag_name('li')
            for li in records:
                anime = AnimeItem()
                try:
                    a = li.find_elements_by_xpath('.//a') # a节点
                    p = li.find_element_by_xpath('.//p')
                    anime['link'] = a[0].get_attribute('href')
                    anime['_id'] = anime['link'].split('/')[-2][2:]
                    anime['cover'] = [a[0].find_element_by_xpath('.//div[1]/img').get_attribute('src').split('@')[0]]
                    if anime['cover'] == '':
                        continue
                    anime['play_count'] = self.parsePlayCount(a[0].find_element_by_class_name('shadow').text)
                    anime['title'] = a[1].text
                    anime['process'] = p.text
                    anime['source'] = 'bilibili'
                    yield anime
                except Exception as e:
                    print(e)
            if i != self.page:
                self.driver.find_element_by_css_selector("[class='p next-page']").click() # 翻页
                time.sleep(random.random() + 2)
        self.driver.quit()

    # def myParse(self, response):
    #     content = demjson.decode(response.body)
    #     data = content['data']['list']
    #     # print(data)
    #     anime = WebdataItem()
    #     for item in data:
    #         anime['_id'] = item['media_id']  # key
    #         anime['title'] = item['title']  # 名称
    #         anime['link'] = item['link']  # 链接
    #         anime['process'] = item['index_show']  # 更新进度
    #         anime['cover'] = item['cover']  # 封面
    #         anime['play_count'] = self.parsePlayCount(item['order'])  # 播放量
    #         anime['source'] = 'bilibili'
    #         yield anime

    def parsePlayCount(self, count):
        """
        处理播放量：
            统一单位
        :param count:
        :return count:
        """
        if count[-4] == '亿':
            count=count.replace(count[0:-4],str(float(count[0:-4]) * 10000))
            count=count.replace(count[-4],'万')
        return count

    def scroll(self):
        """
        滑动滚动条：
            克服懒加载的图片
        """
        # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 滑到底部，加载懒加载的图片
        for i in range(1,3):
            self.driver.find_element_by_xpath('/html/body').send_keys(Keys.SPACE)
            time.sleep(random.random()+2)

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

