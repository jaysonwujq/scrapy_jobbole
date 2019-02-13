# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import pymysql.cursors
class MysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = pymysql.connect('localhost', 'root', '', 'testdb', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into testdb(title, url, create_date, fav_nums)
            VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))
        self.conn.commit()


from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors


class MysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool

    @classmethod
    def from_settings(cls,settings):
        dbpool=adbapi.ConnectionPool(
            "pymysql",host=settings["MYSQL_HOST"],db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],password=settings["MYSQL_PASSWORD"],charset="utf8",
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True)
        return cls(dbpool)

    def process_item(self,item,spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrorback(self.handle_error)#处理异常

    def handle_error(self,failure,item,spider):
        #处理异步插入的异常
        print(failure)


    def do_insert(self,cursor,item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        print(insert_sql,params)
        cursor.execute(insert_sql, params)


from scrapy.pipelines.images import ImagesPipeline
class ArticleImagePipeline(ImagesPipeline):
    '''
    对图片的处理
    '''
    def item_completed(self, results, item, info):

        for ok ,value in results:
            if ok:
                image_file_path = value["path"]
                item['front_image_path'] = image_file_path
            else:
                item['front_image_path'] = ""


        return item