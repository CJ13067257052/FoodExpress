# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import FEFoodItem
from .items import FERestaurantItem
from .items import FEPlatform
import pymysql


from twisted.enterprise import adbapi


class RestaurantPipeline(object):
    count = 0
    def __init__(self,dbpool):
        self.dbpool = dbpool




    @classmethod
    def from_settings(self, settings):
        # 先将setting中连接数据库所需内容取出，构造一个地点

        # dbparms = {
        #     host = settings["MYSQL_HOST"],
        #     port=3306,
        #     user='root',
        #     passwordsettings["MYSQL_PASSWORD"],
        #     db=settings["MYSQL_DBNAME"],
        #     charset="utf-8"
        #     #'cursorclass': pymysql.cursors.DictCursor,
        # }

        try:
            # 生成连接池
            #dbpool = adbapi.ConnectionPool('pymysql', dbparms)
            dbpool = adbapi.ConnectionPool("pymysql", host=settings["MYSQL_HOST"], db=settings["MYSQL_DBNAME"],
                                           user=settings["MYSQL_USER"], password=settings["MYSQL_PASSWORD"],
                                           charset="utf8",
                                           cursorclass=pymysql.cursors.DictCursor,
                                           use_unicode=True)
            return self(dbpool)
        except Exception as e:
            print(e)





    def process_item(self, item, spider):
        # 使用Twisted异步的将Item数据插入数据库
        query = self.dbpool.runInteraction(self.do_insert, item)
        #query.addCallbacks(self.handle_error, item, spider)  # 这里不往下传入item,spider，handle_error则不需接受,item,spider)
        if self.count < 5:
            filename = '%s.txt' % self.count
            with open(filename,'w') as f :
                f.write(item['restaurant_name'])
            self.count += 1



    def do_insert(self, cursor, item):
        # 执行具体的插入语句,不需要commit操作,Twisted会自动进行
        insert_sql = """
             insert into fe_restaurant(restaurant_name,description,address,deliver_fee,
                 deliver_min_money,platform_id
                 )
             VALUES(%s,%s,%s,%f,%f,%d)
        """
        cursor.execute(insert_sql, (item["restaurant_name"], item["address"],
                                    item["description"], item["deliver_fee"], item["deliver_min_money"],
                                    item["platform_id"]))

    # def handle_error(self, failure, item, spider):
    #     # 出来异步插入异常
    #     print(failure)
