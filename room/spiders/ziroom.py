# -*- coding: utf-8 -*-
import pytesseract
import scrapy
import re
import requests
from PIL import Image



class ZiroomSpider(scrapy.Spider):
    name = 'ziroom'
    allowed_domains = ['ziroom.com']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
    start_urls = ['http://www.ziroom.com/z/s100013-r2-p{}/?sort=2'.format(num) for num in range(1, 10)]

    def parse(self, response):
        urls = response.xpath('//div[@class="pic-box"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request("http:" + url, callback=self.parse_info)

    def parse_info(self, response):
        payurls = response.xpath('//div[@class="Z_price"]/i/@style').extract()
        Z_name = response.xpath('/html/body/section/aside/h1/text()').extract_first()
        Z_home_b = response.xpath('/html/body/section/aside/div[3]/div[1]/dl[1]/dd/text()').extract_first()
        chaoxiang = response.xpath('/html/body/section/aside/div[3]/div[1]/dl[2]/dd/text()').extract_first()
        huxing = response.xpath('/html/body/section/aside/div[3]/div[1]/dl[3]/dd/text()').extract_first()
        weizhi = response.xpath('/html/body/section/aside/div[3]/ul/li[1]/span[2]/span/text()').extract_first()
        louceng = response.xpath('//ul[@class="Z_home_o"]/li[2]/span[@class="va"]/text()').extract_first()
        dianti = response.xpath('//ul[@class="Z_home_o"]/li[3]/span[@class="va"]/text()').extract_first()
        gongnuan = response.xpath('//ul[@class="Z_home_o"]/li[5]/span[@class="va"]/text()').extract_first()
        qianyue = response.xpath('//*[@id="live-tempbox"]/ul/li[2]/span[2]/text()').extract_first()
        if payurls:
            yield  {
                "标题": Z_name[5:],
                "价格": self.NumUrl(payurls),
                "面积": Z_home_b,
                "朝向": chaoxiang,
                "户型": huxing,
                "位置": weizhi,
                "楼层": louceng,
                "电梯": dianti,
                "供暖": gongnuan,
                "签约": qianyue,
                "链接": response.url,
            }

    def NumUrl(self, datas):
        Nnum = []
        url=re.findall(r"url\((.+)\)", datas[0])[0]
        with open("Img.jpg", "wb")as file:
            file.write(requests.get("http:"+url, headers=self.headers).content)
        for data in datas:
            dataNumUrl = re.findall(r"background-position:-(.+)px;", data)[0]
            NumList = self.ImgNum(dataNumUrl)  # 获得图片的对应数字
            Nnum.append(NumList)
        # print("-------------------------------------------------------------------------","".join(Nnum))
        return "".join(Nnum)

    def ImgNum(self, num):
        im = Image.open("Img.jpg")
        # 图片的宽度和高度
        img_size = im.size
        print("图片宽度和高度分别是{}".format(img_size))
        '''
        #4190
        裁剪：传入一个元组作为参数
        元组里的元素分别是：
        （距离图片左边界距离x， 
        距离图片上边界距离y，
        距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h）
        '''
        # 截取4290
        x = float(num) * 1.2
        y = 0
        w = img_size[1]
        h = img_size[1]
        region = im.crop((x, y, x + w, y + h))
        # region.show()
        region.save("IMG.png")
        ast = pytesseract.image_to_string(Image.open("IMG.png"), lang="eng",
                                          config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')
        return ast
