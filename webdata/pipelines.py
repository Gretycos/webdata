# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from webdata.model import loadSession


class WebdataPipeline(object):
    def __init__(self):
        self.session = loadSession()

    def process_item(self, item, spider):
        a = anime.Anime(
            id=item['_id'],
            title=item['title'],
            link=item['link'],
            process=item['process'],
            cover=item['cover'],
            play_count=item['play_count'],
            source=item['source']
        )
        try:
            self.session.add(a)
            self.session.commit()
            print("保存成功")
        except:
            print("id已存在:[{}]".format(item['_id']))
            self.session.rollback()
        # print(item)
        return item

    def close_spider(self,spider):
        print("爬虫结束")
        self.session.close()
