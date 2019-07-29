# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql as pq


class SchoolsinfoPipeline(object):
    def process_item(self, item, spider):
        return item



class MongoPipeline(object):
    def __init__(self):
        self.conn = pq.connect(host='localhost', user='root',
                               passwd='123456789', db='new_schools', charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        school_id = item.get("school_id", "N/A")  # 有的图书有数据项缺失，这里做了容错处理
        province_id = item.get("province_id", "N/A")
        max = item.get("max", "N/A")
        min = item.get("min", "N/A")
        average = item.get("average", "N/A")
        filing = item.get("filing", "N/A")
        type = item.get("type", "N/A")
        batch = item.get("batch", "N/A")
        min_section = item.get("min_section", "N/A")
        add_id = item.get("add_id", "N/A")
        local_batch_name = item.get("local_batch_name", "N/A")
        proscore = item.get("proscore", "N/A")
        id = item.get('id', 0)

        sql = "insert into quickstart_schools(school_id, province_id, max, min, average, filing, type, batch, min_section, add_id, local_batch_name, proscore, id) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cur.execute(sql, (school_id, province_id, max, min, average, filing, type, batch, min_section, add_id, local_batch_name, proscore, id))
        self.conn.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

