from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter

class CustomCsvItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter
        
        super(CustomCsvItemExporter, self).__init__(*args, **kwargs)
