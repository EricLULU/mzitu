# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy 
from scrapy.pipelines.images import ImagesPipeline
import requests
class MizituPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        print("执行到了pipeline")
        referer = item['url']
        print("来源链接:", referer)
        url = item['image_urls']
        print("图片下载链接是：",url)
        
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'DNT':'1',
            'Host':'i.meizitu.net',
            'Referer':'http://www.mzitu.com/147738/3',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            }
        headers['Referer'] = referer
        r = requests.get(url,headers=headers)
        filename = r"E:\srcpro\meizitu\PICTURE" + '\\' + url.split('/')[-1]
        with open(filename, 'wb') as f:
            f.write(r.content)
            print("字节长度:", len(r.content))
            print("保存成功")
        
        yield scrapy.Request(url=url, meta={'item':item, 'Referer': referer})
        