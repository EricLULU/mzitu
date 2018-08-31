# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MizituItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tag_name = scrapy.Field()     #当前所在位置， 用于大文件夹
    album_name = scrapy.Field()   #相册名字
    url = scrapy.Field()          #单个图片链接
    image_urls = scrapy.Field()   #图片下载链接， 用于文件命名