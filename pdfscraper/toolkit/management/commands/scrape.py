from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg, Max, Min, Count, Sum, StdDev
import subprocess
import os
import calendar as cal
import copy
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils import timezone

# Import Project models
from spiders.models  import Spider, SpiderUrl, SpiderRule
from dataitems.models  import DataItem
from toolkit.toolkit.spiders.spiders import CustomSpider
from scrapesessions.models import SpiderSession

# Import Python libraries
from datetime import date, datetime
import time as sleeper

# Import Scrapy Requirements
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings



def bash_command(cmd):
    subprocess.Popen(['/bin/bash', '-c', cmd], shell=True)
    

def scrape_spider(myspider):
    from django.conf import settings
    start_time = timezone.now()
    
    # Save spider session
    new_spider_session = SpiderSession(time_started=start_time)
    new_spider_session.save()
    
    print "Fetch Spider details"
    input_required_filetype = "pdf"
    
    print "Create spider for %s" % myspider.title
    spider1 = CustomSpider(spidermodel = myspider,
                           spidersession = new_spider_session,
                           input_required_filetype=input_required_filetype,
                           input_allowed_domains=list(SpiderUrl.objects.filter(spider=myspider, url_type="ALLOWED_DOMAINS").values_list('url', flat=True)),
                           input_start_urls=list(SpiderUrl.objects.filter(spider=myspider, url_type="START_URL").values_list('url', flat=True)),
                           input_spider_name=myspider.title,
                           input_denied_files=settings.DENY_FILE_TYPES,
                           input_allow_rules=list(SpiderRule.objects.filter(spider=myspider, rule_type="ALLOW").values_list('regexp', flat=True)),
                           input_deny_rules=list(SpiderRule.objects.filter(spider=myspider, rule_type="DENY").values_list('regexp', flat=True)))
    
    print "\n\n\n\n**********"
    print "Spider Rules"
    print spider1.rules
    
    print "Spider Allowed Domains"
    print spider1.allowed_domains
    
    print "Spider Start Urls"
    print spider1.start_urls
    
    print "Spider Required Filetypes"
    print spider1.required_filetypes
    
    print "Spider Name"
    print spider1.name
    print "**********\n\n\n\n"
    
    print "Get settings"
    settings = get_project_settings()
    
    print "Create crawlser"
    crawler = Crawler(settings)
    
    print "Connect crawler to reactor"
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    
    print "Configure crawler"
    crawler.configure()
    
    print "Crawl spider"
    crawler.crawl(spider1)
    
    print "Start crawler"
    crawler.start()
    
    print "Make logs"
    #log.start()
    
    print "Run reactor"
    reactor.run() # the script will block here until the spider_closed signal was sent
    
    end_time = timezone.now()
    time_taken = round((end_time - start_time).total_seconds() / 60, 4)
    print "Completed scrape"
    print "Total time: %s minutes " % str(time_taken)       
    num_data = DataItem.objects.filter(session=new_spider_session).count()
    print "Number of new pdfs found: " + str(num_data)
    
    # Save spider session
    new_spider_session.time_ended = end_time
    new_spider_session.save()


    
class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--long', '-l', dest='long',
            help='Help for the long options'),
    )
    help = 'Help text goes here'

    def handle(self, **options):
        """
        """
        print "START"
        #sleeper.sleep(3)
        
        
        for spider in Spider.objects.filter(is_enabled=True):
            print spider
            scrape_spider(spider)
            sleeper.sleep(2)
     
        print "END"        