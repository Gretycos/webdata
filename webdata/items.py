# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnimeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()  # key
    title = scrapy.Field()  # 名称
    link = scrapy.Field()  # 链接
    process = scrapy.Field()  # 更新进度
    cover = scrapy.Field()  # 封面
    play_count = scrapy.Field()  # 播放量
    source = scrapy.Field()  # 来源

class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()  # key
    title = scrapy.Field()  # 名称
    link = scrapy.Field()  # 链接
    cover = scrapy.Field()  # 封面
    play_count = scrapy.Field()  # 播放量
    source = scrapy.Field()  # 来源