# -*- coding: utf-8 -*-
import random
import time

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from webdata.items import AnimeItem


class TencentSpider(scrapy.Spider):
    name = 'Tencent_Anime'
    custom_settings = {
        'ITEM_PIPELINES': {
            'webdata.pipelines.AnimePipeline': 400
        }
    }
    allowed_domains = ['v.qq.com']
    start_urls = ['https://v.qq.com/channel/cartoon?listpage=1&channel=cartoon&sort=18&_all=1']
    driver = None
    page = 70  # 爬取页数

    def parse(self, response):
        """
        处理爬虫请求：
            利用selenium模拟浏览器点击、翻页，从结构中抽取出信息
        :param response:
        :return:
        """
        print("启动中...")
        self.driver_init()
        self.driver.get(response.url)
        time.sleep(5)
        print("跳转中...")
        for i in range(1,self.page+1):
            print("正在爬取第{}页...".format(i))
            div = self.driver.find_elements_by_xpath('/html/body/div[5]/div/div[2]/div')
            # print(len(div))
            for list_item in div:
                anime = AnimeItem()
                a = list_item.find_element_by_xpath('./a')
                anime['link'] = a.get_attribute('href')
                anime['title'] = a.get_attribute('title')
                anime['_id'] = a.get_attribute('data-float')
                anime['cover'] = [a.find_element_by_xpath('./img[1]').get_attribute('src')]
                try:
                    text = a.find_element_by_xpath('./div').text
                    anime['process'] =  text if text[-1] == '集' else '全1集'
                except:
                    anime['process'] = '全1集'
                self.driver.execute_script("window.open('{}')".format(anime['link']))
                self.driver.switch_to.window(self.driver.window_handles[-1])  # 切换窗口
                try:
                    WebDriverWait(self.driver, 0.6, 0.3).until(lambda driver:driver.find_element_by_xpath('//*[@id="container_player"]/div/div[1]/div[1]/div[2]/div[1]/div[1]/a/span'))
                    anime['play_count'] = self.parsePlayCount(self.driver.find_element_by_xpath('//*[@id="container_player"]/div/div[1]/div[1]/div[2]/div[1]/div[1]/a/span').text)
                except Exception as e:
                    print(e)
                    continue
                finally:
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[-1])  # 切换窗口
                # print(title,link,id,cover,process,play_count)
                anime['source'] = 'tencent'
                yield anime
            if i != self.page:
                # self.driver.find_element_by_css_selector("[data-offset='1968']").click()
                self.driver.find_element_by_css_selector("[class='page_next ']").click() # 翻页
                time.sleep(1)
        self.driver.quit()

    def parsePlayCount(self, count):
        """
        处理播放量：
            统一单位、去除不够一万次的动漫
        :param count:
        :return count:
        """
        if count[-6] == '亿':
            count=count.replace(count[0:-6],str(float(count[0:-6]) * 10000))
            count=count.replace(count[-6],'万')
        if '万' not in count:
            raise Exception('播放次数少于1万')
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
