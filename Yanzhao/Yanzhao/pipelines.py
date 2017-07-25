# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


class YanzhaoPipeline(object):
    def process_item(self, item, spider):
        return item

class Newspaperpipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            db='Yanzhao',
                                            user='root',
                                            passwd='password',
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset='utf8',
                                            use_unicode=False
                                            )
        #和数据库链接的部分，实际情况实际考虑

    def handle_error(self, e):
        log.err(e)
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item


    def _conditional_insert(self, tx, item):
            try:
                tx.execute(
                "insert into yanzhaodata (class,title, source, main) \
            values (%s,%s, %s, %s)",
                (item['title'][0],''.join(item['title'][1:]), item['source'][0], ''.join(item['main']))
                )
            except:
                tx.execute("create table yanzhaodata("
                           "class char(50),"
                           "title char(50),"
                           "source char(30),"
                           "main text(65535))")
                tx.execute(
                    "insert into yanzhaodata (class,title, source, main) \
                values (%s,%s, %s, %s)",
                    (item['title'][0], ''.join(item['title'][1:]), item['source'][0], ''.join(item['main']))
                )

