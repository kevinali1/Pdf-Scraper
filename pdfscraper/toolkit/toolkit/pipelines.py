# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from dataitems.models import DataItem

class ToolkitPipeline(object):
    def process_item(self, item, spider):
        return item


class DbInsertPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        
        try:
            item_duplicate = DataItem.objects.get(link = item['link'],
                                                  title = item['title'])
        except DataItem.DoesNotExist:
            new_item = DataItem(date_scraped = item['date'],
                                link = item['link'],
                                referrer = item['referrer'],
                                title = item['title']) 
            new_item.save()
            return item
        