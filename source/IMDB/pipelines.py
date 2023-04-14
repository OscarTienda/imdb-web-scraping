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
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signal=signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open("../../dataset/imdb.csv", "wb")
        self.files[spider] = file
        self.exporter = MyCsvItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class MyCsvItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['delimiter'] = ','
        super().__init__(*args, **kwargs)