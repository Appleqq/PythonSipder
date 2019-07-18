import scrapy
import json
from schoolsInfo.items import SchoolsinfoItem

class schools(scrapy.Spider):
    name = 'schoolsInfo'
    allowed_domains = ['static-data.eol.cn']
    i = 13;
    start_urls = ['https://static-data.eol.cn/www/2.0/schoolprovinceindex/2018/102/13/1/1.json']
    while i <= 44:
        j = 2014
        while j <= 2018:
            k = 30
            while k <= 199:
                n = 1
                while n <= 2:
                    url = 'https://static-data.eol.cn/www/2.0/schoolprovinceindex/' + f'{j}' + '/' + f'{k}' + '/' + f'{i}' + '/' + f'{n}' + '/' + '1.json'
                    print(url)
                    start_urls.append(url)
                    n = n + 1
                k = k + 1
            j = j + 1
        i = i + 1

    def parse(self, response):
        data = json.loads(response.body_as_unicode())

        info = data.get('data')
        info_items = info.get('item')
        for item in info_items:
            item_model = SchoolsinfoItem()
            item_model['id'] = item.get('id')
            item_model['school_id'] = item.get('school_id')
            item_model['province_id'] = item.get('province_id')
            item_model['max'] = item.get('max')
            item_model['min'] = item.get('min')
            item_model['average'] = item.get('average')
            item_model['num'] = item.get('num')
            item_model['type'] = item.get('type')
            item_model['batch'] = item.get('batch')
            item_model['min_section'] = item.get('min_section')
            item_model['add_id'] = item.get('add_id')
            item_model['add_time'] = item.get('add_time')
            item_model['update_id'] = item.get('update_id')
            item_model['update_time'] = item.get('update_time')
            item_model['ansytype'] = item.get('ansytype')
            item_model['local_batch_name'] = item.get('local_batch_name')
            item_model['proscore'] = item.get('proscore')
            yield item_model



