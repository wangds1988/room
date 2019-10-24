# -*- coding: utf-8 -*-
import scrapy


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['http://bj.bendibao.com']
    start_urls = ['http://bj.bendibao.com/zffw/201274/80667_{}.shtm'.format(num) for num in range(1, 10)]

    def parse(self, response):
        datas_didian = response.xpath('string(//div[@class="content"]/p)').extract()
        datas_xiangxixinxi = response.xpath('//div[@class="content"]/p/text()').extract()

        for data1 in datas_didian, datas_xiangxixinxi:
            print(data1)

