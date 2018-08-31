# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from mizitu.items import MizituItem
import time
class MzituSpider(scrapy.Spider):
    name = 'mzitu'
    start_urls = ['http://www.mzitu.com/']
    img_urls = []
    items = MizituItem()
    """
    rules = (
        Rule(LinkExtractor(allow=(r'http://www.mzitu.com/\d{1,6}',), deny=(r'http://www.mzitu.com/\d{1,6}/\d{1,6}')), callback='self.parse_item', follow=True),
    )
    """

    def parse(self, response):
        """
            获取大标签的链接，如性感妹子，日本妹子等
        """
        li_list = response.css('#menu-nav li')
        for li in li_list:
            link = li.css("a::attr(href)").extract_first()                 #大标签的名字
            self.items['tag_name'] = li.css("a::text").extract_first()  #获取标签名字
            yield scrapy.Request(url=link, callback=self.parse_mid)
        #print(response.url)

    def parse_mid(self, response):
        """
            获取大标签下的每个相册的链接
        """
        li_list = response.css('#pins li')
        for li in li_list:
            url = li.css('a::attr(href)').extract_first()
            print("相册链接-->>", url)
            self.items['album_name'] = li.css('span a::text').extract_first()   #获取相册的名字
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self,response):
        """
            获取每个相片的链接
        """
        try:
            max_num = response.css('.pagenavi a')[-2].css("span::text").extract_first()
        except:
            max_num = 10
        else:
            try:
                m_num = int(max_num)
            except:
                m_num = 10
        print("照片最大数:", m_num)
        for i in range(1, int(m_num)+1):
            url = response.url + '/' + str(i)
            #print("相册链接：", response.url)
            print("单个相片的链接-->>", url)
            yield scrapy.Request(url, callback=self.parse_url)


    def parse_url(self, response):
        """
            获取每个照片的下载页链接
        """
        url = response.css('.main-image img::attr(src)').extract_first()
        self.items['url'] = response.url       #获取单个相片链接
        self.items['image_urls'] = url         #获取单个图片下载的链接
        yield self.items