from scrapy.crawler import CrawlerProcess
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.project import get_project_settings

# 根据项目配置获取 CrawlerProcess 实例
process = CrawlerProcess(get_project_settings())

# 获取 spiderloader 对象，以进一步获取项目下所有爬虫名称
spider_loader = SpiderLoader(get_project_settings())

for spidername in spider_loader.list():
    process.crawl(spidername)

# 执行
process.start()