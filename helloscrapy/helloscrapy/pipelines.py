# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class HelloscrapyPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(
            host='127.0.0.1',
            unix_socket='/tmp/mysql.sock',
            user='root',
            passwd='',
            db='mysql',
            charset='utf8'
        );
        cur = conn.cursor()

        sql = 'INSERT INTO ' \
              'scrapy.scp(item_no, object_class, protocol, description) ' \
              'VALUES (%s, %s, %s, %s)'
        try:
            cur.execute(
                sql,
                (
                    item['item_no'],
                    item['object_class'],
                    item['protocol'],
                    item['description']
                )
            )
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()

        return item
