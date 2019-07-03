import scrapy
import json
from schoolsInfo.items import SchoolsinfoItem

class schools(scrapy.Spider):
    name = 'schoolsInfo'
    allowed_domains = ['static-data.eol.cn']

    def start_requests(self):
        urls = ['https://static-data.eol.cn/www/2.0/schoolprovinceindex/2018/102/13/1/1.json']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        data = json.loads(response.body)

        info = data.get('data')
        info_items = info.get('item')
        for item in info_items:
            item_model = SchoolsinfoItem()
            item_model.id = item.get('id')
            item_model.school_id = item.get('school_id')
            item_model.max = item.get('max')

            yield item_model

