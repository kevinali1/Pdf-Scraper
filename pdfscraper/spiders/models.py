from django.db import models, IntegrityError
from django.db.models import Manager
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType


from datetime import date, datetime, timedelta


class SpiderCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    class Meta:
        verbose_name_plural = 'Spider Categories'
        verbose_name = 'Spider Category'
        ordering = ['name']
   
    def __unicode__(self):
        return u'%s' % (unicode(self.name))



class Spider(models.Model):
    """
    Represents a site to be scraped
    """
   
    title = models.CharField(max_length=255, unique=True)
    is_enabled = models.BooleanField(default=False, help_text="Status")
    category = models.ManyToManyField(SpiderCategory)
    
    class Meta:
        verbose_name_plural = 'Spiders'
        verbose_name = 'Spider'
        ordering = ['title']
   
    def __unicode__(self):
        return u'%s' % (unicode(self.title))


class SpiderUrl(models.Model):
    """
    Represents a url for the spider
    """
   
    spider = models.ForeignKey(Spider)
    url = models.URLField()
    
    URL_TYPES = (
        (u'START_URL', u'Start Url'),
        (u'ALLOWED_DOMAINS', u'Allowed Domain'),
    )
    url_type = models.CharField(max_length=255, choices=URL_TYPES)    
    
    
    class Meta:
        verbose_name_plural = 'Spider Urls'
        verbose_name = 'Spider Urls'
        unique_together = ['url', 'url_type']
   
    def __unicode__(self):
        return u'%s' % (unicode(self.url))



class SpiderRule(models.Model):
    """
    Represents a rule for the spider
    """
   
    spider = models.ForeignKey(Spider)
    regexp = models.CharField(max_length=255, unique=True)
    
    RULE_TYPES = (
        (u'ALLOW', u'Allow Rule'),
        (u'DENY',  u'Deny Rule'),
    )
    rule_type = models.CharField(max_length=255, choices=RULE_TYPES)  
    
    
    class Meta:
        verbose_name_plural = 'Spider Rules'
        verbose_name = 'Spider Rule'
        unique_together = ['spider', 'regexp', 'rule_type']
   
    def __unicode__(self):
        return u'%s' % (unicode(self.id))