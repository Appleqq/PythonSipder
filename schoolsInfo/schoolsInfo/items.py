# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SchoolsinfoItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    school_id = scrapy.Field()
    province_id = scrapy.Field()
    max = scrapy.Field()
    min = scrapy.Field()
    average = scrapy.Field()
    num = scrapy.Field()
    type = scrapy.Field()
    batch = scrapy.Field()
    min_section = scrapy.Field()
    add_id = scrapy.Field()
    add_time = scrapy.Field()
    update_id = scrapy.Field()
    update_time = scrapy.Field()
    ansytype = scrapy.Field()
    local_batch_name = scrapy.Field()
    proscore = scrapy.Field()
    pass
