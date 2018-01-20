# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import FEFoodItem
from .items import FERestaurantItem
from .items import FEPlatform
from .items import FEFoodCategoryItem
import pymysql

from scrapy.utils.project import get_project_settings

from .util.DBHelper import DBHelper


#from twisted.enterprise import adbapi


class RestaurantPipeline(object):
    def process_item(self, item, spider):
        # settings = get_project_settings()
        # dbHelper = DBHelper.from_settings(settings)
        if spider.name == 'eleme_restaurant':
            dbHelper = DBHelper.getDBHelper()
            dbHelper.insertRestaurant(item)


class ElemePipeline(object):
    def process_item(self, item, spider):
        # settings = get_project_settings()
        # dbHelper = DBHelper.from_settings(settings)
        dbHelper = DBHelper.getDBHelper()
        if spider.name == 'eleme_food':
            #print('种类名称item name ' % item['category_name'])
            dbHelper.insert(item)
        if spider.name == 'eleme_restaurant':
            dbHelper.insertRestaurant(item)
