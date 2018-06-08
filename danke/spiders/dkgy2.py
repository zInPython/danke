# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from danke.items import DankeItem


class DankeSpider(CrawlSpider):

    # 爬虫名
    name = 'dkgy2'

    # 允许抓取的url
    allowed_domains = ['dankegongyu.com']

    custom_settings = {'DOWNLOAD_DELAY': 0.2}

    # 请求开始的url
    start_urls = ['https://www.dankegongyu.com/room/sz']


    # rules属性
    rules = (

        # 定义规则，抓取符合要求的url
        # allow是允许爬取的规则，后面的内容是正则表达式，匹配页面中所有符合匹配规则的a标签
        # callback是回调函数，用于解析抓取到的符合匹配的链接
        # follow：是否跟进，是否继续请求抓取到的链接
        Rule(LinkExtractor(allow=r'page=\d+'), follow=True),

        #编写匹配详情页的规则，抓取到详情页的链接后不用跟进
        Rule(LinkExtractor(allow=r'https://www.dankegongyu.com/room/\d+'), callback='parse_detail', follow=False),
    )

    def parse_detail(self, response):
        """
        解析详情页数据
        :param response:
        :return:
        """
        node_list = response.xpath('//div[@class="room-detail-right"]')
        for node in node_list:
            item = DankeItem()

            # 房间名称
            room_name = node.xpath('./div/h1/text()')
            item['room_name'] = room_name.extract_first()

            # 房间租金
            room_money = node.xpath('./div[@class="room-price"]/div/span').xpath('string(.)').extract_first()

            # 有的房子没有首月租金
            if room_money:
                item['room_money'] = room_money
            else:
                room_money = node.xpath('./div[@class="room-price hot"]/div/div[@class="room-price-num"]/text()').extract_first()
                item['room_money'] = room_money
                print(room_money)

            # 房间面积
            room_area = node.xpath('./*/div[@class="room-detail-box"]/div[1]/label/text()').extract_first().split('：')[-1]
            item['room_area'] = room_area

            # 房间编号
            room_numb = node.xpath('./*/div[@class="room-detail-box"]/div[2]/label/text()').extract_first().split('：')[-1]
            item['room_numb'] = room_numb

            # 房间户型
            room_type = node.xpath('./*/div[@class="room-detail-box"]/div[3]/label/text()').extract_first().split('：')[-1]
            item['room_type'] = room_type

            # 租房方式
            rent_type = node.xpath('./*/div[@class="room-detail-box"]/div[3]/label/b/text()').extract_first().split('：')[
                -1]
            item['rent_type'] = rent_type

            # 所在楼层
            room_floor = node.xpath('./div[@class="room-list-box"]/div[2]/div[2]').xpath('string(.)').extract_first().split('：')[-1]
            item['room_floor'] = room_floor

            # 所在区域
            room_loca = node.xpath('./div[@class="room-list-box"]/div[2]/div[3]/label/div/a[1]/text()').extract_first()
            item['room_loca'] = room_loca

            # 所在楼盘
            estate_name = node.xpath('./div[@class="room-list-box"]/div[2]/div[3]/label/div/a[3]/text()').extract_first()
            item['estate_name'] = estate_name

            yield item

