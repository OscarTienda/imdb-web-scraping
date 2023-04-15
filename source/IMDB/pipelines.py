# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import csv
from scrapy.exporters import CsvItemExporter
from scrapy import signals
from itemadapter import ItemAdapter

class ImdbPipeline:
    def process_item(self, item, spider):
        return item

class MyCsvItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['delimiter'] = ','
        super().__init__(*args, **kwargs)