from multiprocessing import context
from pkg_resources import yield_lines
import scrapy
import os
import ssl

import urllib.request

class CorleoneSpider(scrapy.Spider):
    name = 'corleone'
    # allowed_domains = ['corleone.com']
    start_urls = ['https://pvp.qq.com/web201605/herolist.shtml']
    def parse(self, response):
        host_name = "https://pvp.qq.com/web201605/"
        hero_list = response.xpath('//div[@class="herolist-box"]/div[@class="herolist-content"]/ul/li/a')        
        for link in hero_list:
            href = link.xpath('./@href').extract()[0]
            detail_url = host_name + href
            yield scrapy.Request(detail_url,self.detail_parse)

    file_path = "/Users/Corleone/Desktop/Res/"
    # https:/game.gtimg.cn/images/yxzj/img201606/skin/hero-info/155/155-bigskin-3.jpg
    def detail_parse(self,response):
        message = response.xpath('/html/body/script[10]/text()').extract()[0]
        cname = message.split(',')[0].split(' = ')[1].replace("'", "").strip()
        ename = message.split(',')[1].split(' = ')[1].replace("'", "").replace(";", "").strip()
        heroskin_template = f"https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{ename}/{ename}-bigskin-"
        if not os.path.exists(self.file_path+cname):
            os.makedirs(self.file_path+cname)
        skins = response.xpath('//div[@class="pic-pf"]/ul/@data-imgname').extract()[0]
        skin_list = skins.split("|")
        
        temp_list = []
        for skin in skin_list:
            temp_list.append(skin.split("&")[0])
        for index in range(0, len(temp_list)):
            skin_name = temp_list[index].split("&")[0]
            file_name = '{}{}{}{}'.format(self.file_path+cname,os.sep,skin_name,".jpg")
            file_link = heroskin_template+"{0}.jpg".format(index+1)
            ssl._create_default_https_context = ssl._create_unverified_context
            urllib.request.urlretrieve(url=file_link,filename=file_name)