# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class FERestaurantItem(scrapy.Item):
    id = scrapy.Field()
    restaurant_name = scrapy.Field()         #饭店名
    address = scrapy.Field()                #饭店地址
    open_time = scrapy.Field()               #营业时间
    description = scrapy.Field()            #说明
    deliver_fee = scrapy.Field()             #送餐费用
    deliver_min_money = scrapy.Field()        #最少起送餐费
    platform_id = scrapy.Field()             #平台ID
    # latitude = scrapy.Field()                #经度
    # longitude = scrapy.Field()               #纬度

class fe_placeRestaurant(scrapy.Item):
    search_place_id = scrapy.Field()         #查询地点
    restaurant_id = scrapy.Field()           #饭店ID
    distance = scrapy.Field                  #饭店距离查询点距离


class FEFoodItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()                   #餐饮名称
    price = scrapy.Field()                  #价钱
    category = scrapy.Field()               #类别
    description = scrapy.Field()            #备注
    month_sales = scrapy.Field()            #月销售
    rating_count = scrapy.Field()           #评论数量
    rating = scrapy.Field()                 #评价星
    restaurant_id = scrapy.Field()          #饭店ID
    platform_id = scrapy.Field()            #平台ID

class FEPlatform(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()                   #平台名
    description = scrapy.Field()            #说明


class FESearchPlace(scrapy.Item):
    id = scrapy.Field()
    city = scrapy.Field()                   #城市
    place = scrapy.Field()                  #搜索地名
    latitude = scrapy.Field()               #经度
    longitude = scrapy.Field()              #纬度
    platform_id = scrapy.Field()            #平台ID
