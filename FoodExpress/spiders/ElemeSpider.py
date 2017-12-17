#coding=utf-8

import  scrapy
import json
from ..items import FEFoodItem
from ..items import FEPlatform
from ..items import FERestaurantItem

class FoodSpider(scrapy.Spider):
    name="eleme"

    def start_requests(self):
        #饿了么数据
        #所有店家
        #urls = ['https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=ww0y02qh73v&latitude=34.8068&limit=24&longitude=113.57406&offset=24&terminal=web']
        #所有美食外卖店家
        urls=['https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=ww0y02qh73v&latitude=34.8068&limit=24&longitude=113.57406&offset=0&restaurant_category_ids%5B%5D=-100&sign=1511773470908&terminal=web']
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

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def processItem(item):
        return item


    def parse(self, response):
        sites = json.loads(response.body_as_unicode())
        for site in sites:
            restaurantItem = FERestaurantItem()
            restaurantItem['restaurant_name'] = site['name']
            restaurantItem['address'] = site['address']
            restaurantItem['open_time'] = site['opening_hours'][0]
            restaurantItem['description'] = site['description']
            restaurantItem['deliver_fee'] = site['float_delivery_fee']
            restaurantItem['deliver_min_money'] = site['float_minimum_order_amount']
            restaurantItem['platform_id'] = 2       #当前只有饿了么
            yield restaurantItem



        # page = response.url.split("/")[-2]
        #
        # filename = '%s.txt' % page
        # a = sites[0]["opening_hours"][0]
        # with open(filename,'w') as f :
        #     f.write(a)
        # self.log("save file %s" % filename)

