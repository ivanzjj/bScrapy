from collections import defaultdict

from scrapy import signals
from spiders.custom_csv_item_exporter import CustomCsvItemExporter

def item_type(item):
    return type(item).__name__.replace('Item','').lower()  # TeamItem => team
    
class BscrapyPipeline(object):
    SaveTypes = ['home','new']

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline
        
    def spider_opened(self, spider):
        self.files = dict([ (name, open(name+'.csv','w+b')) for name in self.SaveTypes ])
        self.exporters = dict([ (name, CustomCsvItemExporter(self.files[name])) for name in self.SaveTypes])
        [e.start_exporting() for e in self.exporters.values()]
        
    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        what = item_type(item)
        if what in set(self.SaveTypes):
            self.exporters[what].export_item(item)
        return item

