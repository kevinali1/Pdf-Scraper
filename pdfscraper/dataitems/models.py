from django.db import models, IntegrityError
from django.db.models import Manager
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

# Import python libraries
import urllib

# Import django models
from spiders.models import Spider
from scrapesessions.models import SpiderSession

class DataItem(models.Model):
    """
    Represents a scraped data item
    """
    
    spider = models.ForeignKey(Spider)
    date_scraped = models.DateTimeField()
    link = models.URLField()
    referrer = models.URLField()
    title = models.CharField(max_length=255)
    session = models.ForeignKey(SpiderSession, blank=True, null=True)
    
    # Some optional stored metadata
    filename = models.CharField(max_length=255, blank=True, null=True)
    filesize = models.PositiveIntegerField(blank=True, null=True)
    last_modification_date = models.DateTimeField(blank=True, null=True)
    
    
    class Meta:
        verbose_name_plural = 'Data Items'
        verbose_name = 'Data Item'
        ordering = ['-date_scraped', 'referrer']
        unique_together = ['link', 'title']

    def __unicode__(self):
        return u'%s, %s,  -  %s' % (unicode(self.date_scraped), 
                                    unicode(self.spider.title), 
                                    unicode(self.title))
    
    def get_filename(self):
        name_components = self.link.split('/')
        if ".pdf" in name_components[-1]:
            return name_components[-1]
    
    def set_cached_data(self, with_url_data=False):
        if self.filename == None:
            self.filename = self.get_filename()
        
        if self.filesize == None or self.last_modification_date == None and with_url_data == True:
            try:
                data = urllib.urlopen(self.link)
            except:
                data = None
                
            try:    
                filesize_string = data.info()['Content-Length']
                self.filesize = int(filesize_string)
            except:
                self.filesize = None
            
            try:
                last_modification_date_string = data.info()['Last-Modified']
                self.last_modification_date = datetime.strptime(last_modification_date_string, '%a, %d %b %Y %H:%M:%S %Z')
            except:
                self.last_modification_date = None
                
        
    
    def simple_save(self, *args, **kwargs):
        super(DataItem, self).save(*args, **kwargs) # Call the "real" save() method.