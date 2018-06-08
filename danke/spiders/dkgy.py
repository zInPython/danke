# -*- coding: utf-8 -*-
import scrapy
from danke.items import DankeItem

class DkgySpider(scrapy.Spider):
    name = 'dkgy'

    allowed_domains = ['dankegongyu.com']

    custom_settings = {'DOWNLOAD_DELAY': 0.2}

    page = 1

    base_url = 'http://www.dankegongyu.com/room/sz?page='

    # 初始抓取的url
    start_urls = [base_url + str(page)]

    def parse(self, response):
        """
        获取详情页链接
        :param response:
        :return:
        """
        # 获取详情页链接
        link_list = response.xpath('//div[@class="r_lbx_cena"]/a/@href').extract()

        if not link_list:
            return

        for link in link_list:

            yield scrapy.Request(url=link, callback=self.detail_parse)

        self.page += 1
        # 继续访问下一页中的链接
        next_page = self.base_url + str(self.page)
        yield scrapy.Request(url=next_page, callback=self.parse)

    def detail_parse(self, response):
        node_list = response.xpath('//div[@class="room-detail-right"]')
        for node in node_list:
            item = DankeItem()

            # 房间名称
            room_name = node.xpath('./div/h1/text()')
            item['room_name'] = room_name.extract_first()

            # 房间租金
            room_money = node.xpath('./div[@class="room-price"]/div/span').xpath('string(.)').extract_first()
            item['room_money'] = room_money

            # 房间面积
            room_area = node.xpath('./*/div[@class="room-detail-box"]/div[1]/label/text()').extract_first().split('：')[
                -1]
            item['room_area'] = room_area

            # 房间编号
            room_numb = node.xpath('./*/div[@class="room-detail-box"]/div[2]/label/text()').extract_first().split('：')[
                -1]
            item['room_numb'] = room_numb

            # 房间户型
            room_type = node.xpath('./*/div[@class="room-detail-box"]/div[3]/label/text()').extract_first().split('：')[
                -1]
            item['room_type'] = room_type

            # 租房方式
            rent_type = \
            node.xpath('./*/div[@class="room-detail-box"]/div[3]/label/b/text()').extract_first().split('：')[
                -1]
            item['rent_type'] = rent_type

            # 所在楼层
            room_floor = \
            node.xpath('./div[@class="room-list-box"]/div[2]/div[2]').xpath('string(.)').extract_first().split('：')[-1]
            item['room_floor'] = room_floor

            # 所在区域
            room_loca = node.xpath('./div[@class="room-list-box"]/div[2]/div[3]/label/div/a[1]/text()').extract_first()
            item['room_loca'] = room_loca

            # 所在楼盘
            estate_name = node.xpath(
                './div[@class="room-list-box"]/div[2]/div[3]/label/div/a[3]/text()').extract_first()
            item['estate_name'] = estate_name

            yield item