from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

def item_type(item):
    return type(item).__name__.replace('Item','').lower()  # TeamItem => team
    
class BscrapyPipeline(object):
    SaveTypes = ['team','club','event', 'match']
    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        self.files = dict([ (name, open(name+'.csv','w+b')) for name in self.SaveTypes ])
        self.exporters = dict([ (name,CsvItemExporter(self.files[name])) for name in self.SaveTypes])
        [e.start_exporting() for e in self.exporters.values()]
        
    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        what = item_type(item)
        if what in set(self.SaveTypes):
            self.exporters[what].export_item(item)
        return item

