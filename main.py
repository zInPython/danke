
import os
import time

while True:
    """
    每隔20*60*60 自动爬取一次，实现自动更新
    """
    os.system("scrapy crawl dkgy3")
    time.sleep(20*60*60)


# from scrapy import cmdline
# cmdline.execute("scrapy crawl dkgy3".split())