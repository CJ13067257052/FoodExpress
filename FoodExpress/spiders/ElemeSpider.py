#coding=utf-8

import scrapy
import json
from ..items import FEFoodItem
from ..items import FEPlatform
from ..items import FEFoodCategoryItem
from ..items import FERestaurantItem


from ..util.DBHelper import DBHelper


class FoodSpider(scrapy.Spider):
    name = "eleme_food"

    start_url = '''https://www.ele.me/restapi/shopping/v2/menu?restaurant_id=%d'''

    def start_requests(self):
        # 德克士产品

        dbHelper = DBHelper.getDBHelper()
        resIdList = dbHelper.queryRestaurantBySearchPlaceId(2)


        for row in resIdList:
            for d, x in row.items():
                print("查询的饭店ID:%s  " % str(x))
                url = self.start_url % x
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)


    def parse(self, response):
        name = 'a'
        dataList = json.loads(response.body_as_unicode())
        if dataList:
            print("有商品数据")

            #添加商品类别
            index = 0
            urlArr = response.url.split('=')
            print("饭店Id: %s" % urlArr[1])
            restaurant_id = urlArr[1]

            if restaurant_id.isdigit():
                for data in dataList:
                    if index > 0 :      #-1是eleme的热销种类，跟普通种类的商品有重复
                        print("添加商品类别")
                        foodCategory = FEFoodCategoryItem()
                        foodCategory['platform_category_id'] = data['id']
                        foodCategory['platform_id'] = 2 #当前只有饿了么
                        foodCategory['category_name'] = data['name']
                        foodCategory['restaurant_id'] = int(restaurant_id)
                        yield foodCategory
                    index = index + 1

            for cat in dataList:
                for food in cat['foods']:
                    print("添加类别下的商品信息")
                    foodItem = FEFoodItem()
                    foodItem['name'] = food['name']
                    foodItem['price'] = food['specfoods'][0]['price']
                    foodItem['platform_category_id'] = food['category_id']
                    foodItem['category_name'] = cat['name']
                    foodItem['description'] = food['description']
                    foodItem['month_sales'] = food['month_sales']
                    foodItem['rating_count'] = food['rating_count']
                    foodItem['rating'] = food['rating']
                    foodItem['restaurant_id'] = int(restaurant_id)
                    foodItem['platform_id'] = 2
                    yield foodItem

class RestaurantSpider(scrapy.Spider):
    name="eleme_restaurant"
    pageLimit = 24
    pageStart = 0
    count = 0
    latitude = 32.13757
    longitude = 115.0502
    start_url = '''https://www.ele.me/restapi/shopping/restaurants?extras[]=activities&geohash=ww0y02qh73v&latitude=%f
        &limit=%d&longitude=%f&offset=%d&restaurant_category_ids[]=-100&sign=1511773470908&terminal=web'''
    def start_requests(self):
        #饿了么数据
        #所有店家
        #urls = ['https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=ww0y02qh73v&latitude=34.8068&limit=24&longitude=113.57406&offset=24&terminal=web']
        #所有美食外卖店家



        url = (self.start_url % (self.latitude,self.pageLimit,self.longitude,self.pageStart))
        #德克士产品
        #urls=['https://www.ele.me/restapi/shopping/v2/menu?restaurant_id=156050583']


        #User_Agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"  # 浼�瑁呮垚娴忚�堝櫒璁块棶
        #head = ('User-Agent', User_Agent)

        #https://www.ele.me/restapi/shopping/restaurants?extras[]=activities&geohash=ww0y02qh73v&latitude=34.8068&limit=24&longitude=113.57406&offset=120&terminal=web
        #url = 'http://waimai.meituan.com/ajax/poilist?_token=eJxt0luPojAUAOD/wqtk6IXSYrIPouN4GQXRUXAyD4ioiCjWC8hm//u2jpLZZAkJXw/nnNITfiu8u1TqEIiLqsr5JEwgpBQbGBkQqUr4I0YpNIhIW/BpS6l/QsgM1dTNLxlxReATmgioEDDwpT6tCyNd3DKrK5KUzfmc1TUtD+I0iF/SKD5fgv1LeEi1zSGNtDwHN2Am2yxZc0VVFFGXTmQdBkSFFIvY/2UI6ZXIXUzIuItWItVbvRL6R99d4EPINCuxSkYlUglXAk+xqoLKLvAu8JRBKuFKcl8kRczH2RCBj+9DWFYwKTldBqSAqGVyD8jEKU0kR5bIkYln8HN06thpDO9nk53J91IknR/Jp3i9V+pK1CuG2ynk+bbhu9fae5siEM6KtcWT+QcYpQE47zpluIuRNp6Si9MLEqitZrw5sCkpcttpOS5zrVEW+6ml55fxm2/2t674f16Re41Ckg87pfd2acwcp5wW/n6xnI1KfdCz2obNjxOW7bfNzYHP/Va3vQ37dqNHu5ajB4NmWbACOq+cmwsv79sWGvPeerUqV1dv6LkdG33g3t4+nnLXcvEtO9itydjOwB45LvVjnASYRsXhODf4ZHn1wQBdY932NmNvuILzne4lJPLwZehkDbx45wFqBpe0xlumd2oV2g7WSuc2zfwa+6X8+QuiOtWX'

        # formdata = {"classify_type": 910, "sort_type": 0, "price_type": 0, "support_online_pay": 0,
        #             "support_invoice": 0, "support_logistic": 0, "page_offset": 1, "page_size": 20,
        #             "uuid": "Bn5zOJtR9nRDTHLz_0HrTPdrcPxF9bFQPfaQxqjMmyWeM8JoRsgh9UQTXEe8vZQY", "platform": 1,
        #             "partner": 4, "originUrl": "http%3A%2F%2Fwaimai.meituan.com%2Fhome%2Fww0y09kjpkgr","_token":"=eJxt0luPojAUAOD/wqtk6IXSYrIPouN4GQXRUXAyD4ioiCjWC8hm//u2jpLZZAkJXw/nnNITfiu8u1TqEIiLqsr5JEwgpBQbGBkQqUr4I0YpNIhIW/BpS6l/QsgM1dTNLxlxReATmgioEDDwpT6tCyNd3DKrK5KUzfmc1TUtD+I0iF/SKD5fgv1LeEi1zSGNtDwHN2Am2yxZc0VVFFGXTmQdBkSFFIvY/2UI6ZXIXUzIuItWItVbvRL6R99d4EPINCuxSkYlUglXAk+xqoLKLvAu8JRBKuFKcl8kRczH2RCBj+9DWFYwKTldBqSAqGVyD8jEKU0kR5bIkYln8HN06thpDO9nk53J91IknR/Jp3i9V+pK1CuG2ynk+bbhu9fae5siEM6KtcWT+QcYpQE47zpluIuRNp6Si9MLEqitZrw5sCkpcttpOS5zrVEW+6ml55fxm2/2t674f16Re41Ckg87pfd2acwcp5wW/n6xnI1KfdCz2obNjxOW7bfNzYHP/Va3vQ37dqNHu5ajB4NmWbACOq+cmwsv79sWGvPeerUqV1dv6LkdG33g3t4+nnLXcvEtO9itydjOwB45LvVjnASYRsXhODf4ZHn1wQBdY932NmNvuILzne4lJPLwZehkDbx45wFqBpe0xlumd2oV2g7WSuc2zfwa+6X8+QuiOtWX"
        #             },

        #yield scrapy.Request(url=url,method="POST",cookies=formdata,callback=self.parse)

        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)

    def processItem(item):
        return item


    def parse(self, response):
        dataList = json.loads(response.body_as_unicode())
        if dataList:
            print("有数据")
            #如果查询结果有数据,则更新分页数据
            self.pageStart = self.pageStart + self.pageLimit
            #插入查询地点记录

            #插入饭店信息
            for data in dataList:
                restaurantItem = FERestaurantItem()
                restaurantItem['restaurant_name'] = data['name']
                restaurantItem['address'] = data['address']
                restaurantItem['open_time'] = data['opening_hours'][0]
                restaurantItem['description'] = data['description']
                restaurantItem['deliver_fee'] = data['float_delivery_fee']
                restaurantItem['deliver_min_money'] = data['float_minimum_order_amount']
                restaurantItem['latitude'] = data['latitude']
                restaurantItem['longitude'] = data['longitude']
                restaurantItem['platform_id'] = 2       #当前只有饿了么
                restaurantItem['search_place_id'] = 2       #搜索位置id
                restaurantItem['distance'] = data['distance']
                restaurantItem['platform_restaurant_id'] = data['id']
                self.count = self.count + 1
                yield restaurantItem
            next_url = (self.start_url % (self.pageLimit, self.pageStart))
            yield scrapy.Request(next_url, callback=self.parse)
        else:
            print("没有数据，当前最大分页值 %d" % (self.pageStart))
            print("总共获取到%d" % self.count)


