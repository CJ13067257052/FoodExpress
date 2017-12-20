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

        try:
            # 生成连接池
            #dbpool = adbapi.ConnectionPool('pymysql', dbparms)
            # dbpool = adbapi.ConnectionPool("pymysql", host=settings["MYSQL_HOST"], db=settings["MYSQL_DBNAME"],
            #                                user=settings["MYSQL_USER"], password=settings["MYSQL_PASSWORD"],
            #                                charset="utf8",
            #                                cursorclass=pymysql.cursors.DictCursor,
            #                                use_unicode=True)

            # 传入settings参数
            dbparms = dict(
                host=settings["MYSQL_HOST"],
                db=settings["MYSQL_DBNAME"],
                user=settings["MYSQL_USER"],
                passwd=settings["MYSQL_PASSWORD"],
                port=settings["MYSQL_PORT"],
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor,
                use_unicode=True
            )
            dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
            return self(dbpool)
        except Exception as e:
            print(e)





    def process_item(self, item, spider):
        # 使用Twisted异步的将Item数据插入数据库
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 错误处理

        query.addCallbacks(self.handle_error)  # 这里不往下传入item,spider，handle_error则不需接受,item,spider)

        ##同步插入
        # 打开数据库连接
        # db = pymysql.connect(host="39.106.2.29", user="root",password="67891011sy", db="FoodExpress", port=3306,charset='utf8mb4')

        #使用cursor()方法获取操作游标
        # cur = db.cursor()

        #sql = ("insert into fe_restaurant(restaurant_name,description,address,deliver_fee,deliver_min_money,platform_id) value ('%s','%s','%s','%f','%f','%d')"
        #       % (item["restaurant_name"], item["address"],item["description"], item["deliver_fee"], item["deliver_min_money"],item["platform_id"]))

        # try:
        #     cur.execute(insert_sql)  # 执行sql语句
        #     db.commit()
        # except Exception as e:
        #     raise e


    def do_insert(self,cursor, item):
        # 执行具体的插入语句,不需要commit操作,Twisted会自动进行
        # insert_sql = ("insert into fe_restaurant(restaurant_name,description,address,deliver_fee,deliver_min_money,platform_id,latitude,longitude) value ('%s','%s','%s','%f','%f','%d','%f','%f')"
        #        % (item["restaurant_name"], item["address"],item["description"], item["deliver_fee"],item["deliver_min_money"],item["platform_id"]))
        a = 1
        try:
            insert_sql,params = item.get_insert_sql()
        except Exception as e:
            print("插入失败，原因:",e)
        else:
            sql = insert_sql % params
            cursor.execute(sql)
            print('成功插入一条数据！')


        # count = count + 1
        id = cursor.lastrowid
        insert_sql2 = ("insert into fe_placeRestaurant(search_place_id,restaurant_id,distance) value (%d,%d,%f)" %(item['search_place_id'],id,item["distance"]))
        cursor.execute(insert_sql2)


    def handle_error(self, failure):
        #出来异步插入异常
        print("异步插入数据错误")
        print(failure)
