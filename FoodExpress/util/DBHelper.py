
from ..items import FEFoodItem
from ..items import FERestaurantItem
from ..items import FEPlatform
from ..items import FEOrderFood
from ..items import FERestaurantOrder



import pymysql
from scrapy.utils.project import get_project_settings


# from twisted.enterprise import adbapi
from DBUtils.PooledDB import PooledDB

class DBHelper(object):

    __instance = None
    __dbPool = None
    # def __init__(self):
    #     self._conn = self.getConn()
    #     self._cursor = self._conn.cursor()


    @staticmethod
    def getDBHelper():
        if DBHelper.__instance:
            DBHelper.__instance.getConn()
            return DBHelper.__instance
        else:

            DBHelper.__instance = DBHelper()
            DBHelper.__instance.getConn()
            return DBHelper.__instance


    def getConn(self):
        if self.__dbPool is None:
            ###使用dbutils 创建连接池###
            settings = get_project_settings()
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
            self.__dbPool = PooledDB(creator=pymysql, mincached=50, maxcached=500, blocking=True,**dbparms)

    if 0:
        def __init__(self,dbpool):
            self.dbpool = dbpool

        @classmethod
        def from_settings(cls, settings):
            # 先将setting中连接数据库所需内容取出，构造一个地点
            #使用twisted 异步操作数据库 ###
            try:

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
                # dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
                # return cls(dbpool)
            except Exception as e:
                print(e)



    def queryRestaurantBySearchPlaceId(self,searchPlaceId):

        sql = ("select res.platform_restaurant_id from fe_restaurant as res LEFT JOIN fe_place_restaurant "
               "as pr on res.id = pr.restaurant_id where pr.search_place_id = %d" % searchPlaceId)

        try:
            _conn = self.__dbPool.connection()
            _cursor = _conn.cursor()
            _cursor.execute(sql)  # 执行sql语句
            ret = _cursor.fetchall()
            print("查询到结果######")
            # 关闭连接对象
            _conn.close()
            return ret
        except Exception as e:
            raise e



    def insert(self,item):
        insert_sql, params = item.get_insert_sql()
        sql = insert_sql % params
        orderid = 1
        print('订单信息插入SQL %s' % sql)
        #for key, value in item.b.items():
        for value in item.b:
            insert_Child_sql = item.get_insertChild_sql()
            params = (orderid,value)
            sql1 = (insert_Child_sql % params)
            print('订单商品信息插入SQL %s' % sql1)


        if 0:
            _conn = self.__dbPool.connection()
            _cursor = _conn.cursor()
            insert_sql, params = item.get_insert_sql()
            sql = insert_sql % params

            try:
                _cursor.execute(sql)
            except Exception as e:
                _conn.rollback()  # 事务回滚
                _conn.close()
                print('事务处理失败', e)
            else:
                _conn.commit()  # 事务提交
                print('事务处理成功', _cursor.rowcount)
                _cursor.close()
                _conn.close()


    def insertOrder(self,item):
        _conn = self.__dbPool.connection()
        _cursor = _conn.cursor()
        insert_sql, params = item.get_insert_sql()
        sql = insert_sql % params
        try:

            _cursor.execute(sql)
            id = _cursor.lastrowid
            F
            insert_sql2 = (
            "insert into fe_place_restaurant(search_place_id,restaurant_id,distance) value (%d,%d,%f)" % (
                item['search_place_id'], id, item["distance"]))
            _cursor.execute(insert_sql2)
        except Exception as e:
            _conn.rollback()  # 事务回滚
            _conn.close()
            print('事务处理失败', e)
        else:
            _conn.commit()  # 事务提交
            print('事务处理成功', _cursor.rowcount)
            _cursor.close()
            _conn.close()

    def insertRestaurant(self,item):
        ### 使用Twisted异步的将Item数据插入数据库  ###
        # query = self.dbpool.runInteraction(self.do_insert, item)
        # 错误处理
        # query.addCallbacks(self.handle_error)  # 这里不往下传入item,spider，handle_error则不需接受,item,spider)

        ###使用DBUtil 连接池获取连接###

        _conn = self.__dbPool.connection()
        _cursor = _conn.cursor()
        insert_sql, params = item.get_insert_sql()
        sql = insert_sql % params
        try:

            _cursor.execute(sql)
            id = _cursor.lastrowid
            insert_sql2 = ("insert into fe_place_restaurant(search_place_id,restaurant_id,distance) value (%d,%d,%f)" % (
                item['search_place_id'], id, item["distance"]))
            _cursor.execute(insert_sql2)
        except Exception as e:
            _conn.rollback()  # 事务回滚
            _conn.close()
            print('事务处理失败', e)
        else:
            _conn.commit()  # 事务提交
            print('事务处理成功', _cursor.rowcount)
            _cursor.close()
            _conn.close()

    if 0 :
        def do_insert(self, cursor, item):
                # 执行具体的插入语句,不需要commit操作,Twisted会自动进行
                # insert_sql = ("insert into fe_restaurant(restaurant_name,description,address,deliver_fee,deliver_min_money,platform_id,latitude,longitude) value ('%s','%s','%s','%f','%f','%d','%f','%f')"
                #        % (item["restaurant_name"], item["address"],item["description"], item["deliver_fee"],item["deliver_min_money"],item["platform_id"]))
                a = 1
                try:
                    insert_sql, params = item.get_insert_sql()
                except Exception as e:
                    print("插入失败，原因:", e)
                else:
                    sql = insert_sql % params
                    cursor.execute(sql)
                    print('成功插入一条数据！')

                # count = count + 1
                id = cursor.lastrowid
                insert_sql2 = ("insert into fe_placeRestaurant(search_place_id,restaurant_id,distance) value (%d,%d,%f)" % (
                item['search_place_id'], id, item["distance"]))
                cursor.execute(insert_sql2)



        def handle_error(self, failure):
            # 出来异步插入异常
            print("异步插入数据回调结果：%s" % failure)
