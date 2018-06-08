# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
import random
import hashlib
import redis
from scrapy.exceptions import IgnoreRequest
from danke.settings import USER_AGENTS as ua

class DankeSpiderMiddleware(object):
    def process_request(self, request, spider):
        """
        给每一个请求随机分配一个代理
        :param request:
        :param spider:
        :return:
        """
        user_agent = random.choice(ua)
        request.headers['User-Agent'] = user_agent

class DankeRedisMiddleware(object):
    """
    将第一个页面上的每一个url放入redis的set类型中，防止重复爬取
    """
    # 连接redis
    def __init__(self):
        self.redis = redis.StrictRedis(host='39.106.116.21', port=6379, db=3)

    def process_request(self, request, spider):

        # 将来自详情页的链接存到redis中
        if request.url.endswith(".html"):
            # MD5加密详情页链接
            url_md5 = hashlib.md5(request.url.encode()).hexdigest()

            # 添加到redis，添加成功返回True,否则返回False
            result = self.redis.sadd('dk_url', url_md5)

            # 添加失败，说明链接已爬取，忽略该请求
            if not result:
                raise IgnoreRequest

