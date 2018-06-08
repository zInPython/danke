# -*- coding: utf-8 -*-

from datetime import datetime
import pymysql

class DankeSourcePipeline(object):
    def process_item(self, item, spider):
        item['source'] = spider.name
        item['utc_time'] = str(datetime.utcnow())
        return item

class DankePipeline(object):

    def __init__(self):

        self.conn = pymysql.connect(
            host='39.106.116.21',
            port=3306,
            database='dk',
            user='z',
            password='136833',
            charset='utf8'
        )
        # 实例一个游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        sql = ("insert into result_latest(标题, 租金, 面积, "
               "编号, 户型, 出租方式, 楼层, "
               "区域, 楼盘, 抓取时间, 数据来源)"
               "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")


        item = dict(item)

        data = [
                item['room_name'],
                item['room_money'],
                item['room_area'],
                item['room_numb'],
                item['room_type'],
                item['rent_type'],
                item['room_floor'],
                item['room_loca'],
                item['estate_name'],
                item['utc_time'],
                item['source'],
                ]
        self.cursor.execute(sql, data)
        # 提交数据
        self.conn.commit()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
