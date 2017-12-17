# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class FERestaurantItem(scrapy.Item):
    restaurant_name = scrapy.Field()         #饭店名
    address = scrapy.Field()                #饭店地址
    open_time = scrapy.Field()               #营业时间
    description = scrapy.Field()            #说明
    deliver_fee = scrapy.Field()             #送餐费用
    deliver_min_money = scrapy.Field()        #最少起送餐费
    platform_id = scrapy.Field()             #平台ID


class FEFoodItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    month_sales = scrapy.Field()
    rating_count = scrapy.Field()
    rating = scrapy.Field()
    restaurant_id = scrapy.Field()
    platform_id = scrapy.Field()

class FEPlatform(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
