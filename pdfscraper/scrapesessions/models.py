from django.db import models

# Create your models here.
    


class SpiderSession(models.Model):
    """
    Represents a scrape of a particular Spider
    """
    time_started = models.DateTimeField()
    time_ended = models.DateTimeField(blank=True, null=True)
    
    # Store cached data
    total_time = models.FloatField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Spider Sessions'
        verbose_name = 'Spider Session'
        ordering = ['time_started', 'time_ended']
   
    def __unicode__(self):
        return u'Scrape Number: %s' % (unicode(self.id))
    
    def save(self, *args, **kwargs):
        if self.time_started != None and self.time_ended != None:
            try:
                total_time = (self.time_ended - self.time_started).total_seconds()
                self.total_time = float(str(total_time))
            except:
                self.total_time = None
        super(SpiderSession, self).save(*args, **kwargs) # Call the "real" save() method.
