# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DankeItem(scrapy.Item):
    """
    编辑带爬取信息字段
    """
    # 数据来源
    source = scrapy.Field()
    # 抓取时间
    utc_time = scrapy.Field()

    # 房间名称
    room_name = scrapy.Field()
    # 房间租金
    room_money = scrapy.Field()
    # 房间面积
    room_area = scrapy.Field()
    # 房间编号
    room_numb = scrapy.Field()
    # 房间户型
    room_type = scrapy.Field()
    # 租房方式
    rent_type = scrapy.Field()
    # 房间楼层
    room_floor = scrapy.Field()
    # 所在区域
    room_loca = scrapy.Field()
    # 所在楼盘
    estate_name = scrapy.Field()
