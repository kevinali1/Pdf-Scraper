from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
import urllib2

# Import Item
from toolkit.toolkit.items import ToolkitItem

# Import python standard libs
from urlparse import urljoin
from datetime import date, datetime

# Import django models
from django.utils import timezone
from dataitems.models import DataItem


def extend_domains(domain_list):
    output = []
    for domain in domain_list:
        
        # Remove trailing slash
        if domain[-1:] == "/":
            domain = domain[:-1]
        
        # Add whole domain
        output.append(domain)
        
        # Remove http and www
        if domain[:11] == "http://www.":
            output.append(domain.replace("http://www.", ""))
        if domain[:12] == "https://www.":
            output.append(domain.replace("https://www.", ""))
        
        # Remove www
        if domain[:7] == "http://":
            output.append(domain.replace("http://", ""))     
        if domain[:8] == "https://":
            output.append(domain.replace("https://", ""))           
    
    return list(set(output))


class CustomSpider(CrawlSpider):
    name = ""
    allowed_domains = []
    start_urls = []
    required_filetypes = []
    rules = []
    
    def __init__(self,
                 spidermodel=None,
                 spidersession=None,
                 input_required_filetype=None,
                 input_allowed_domains=None,
                 input_start_urls=None,
                 input_spider_name=None,
                 input_denied_files=None,
                 input_allow_rules=None,
                 input_deny_rules=None,
                 *args, **kwargs):
        self.spidermodels = spidermodel
        self.session = spidersession
        self.name = input_spider_name
        self.allowed_domains = extend_domains(input_allowed_domains)
        self.start_urls = input_start_urls
        self.rules = [Rule(SgmlLinkExtractor(allow=input_allow_rules, 
                                             unique=True, 
                                             deny=input_deny_rules + ['.+\.%s' % i for i in input_denied_files]), 
                           callback='parse_item', 
                           follow=True),]
        self.required_filetypes = ["pdf"]
        
        #self.name = "republic"
        #self.allowed_domains = ["republictt.com", "www.republictt.com", "http://www.republictt.com",]
        #self.start_urls = ["http://www.republictt.com", 'http://www.republictt.com/1asp/default.asp']
        #self.rules =  [Rule(SgmlLinkExtractor(allow=('.+republictt.com/.+', ), 
                                              #unique=True, 
                                              #deny=('.+\.flv')), 
                            #callback='parse_item', 
                            #follow=True)]
        #self.required_filetypes = ["pdf"]
        
        super(CustomSpider, self).__init__(*args, **kwargs)
        
    
    def parse_item(self, response):
        self.log('Hi, this is an item page!')
        print "Scraping a new page and searching"
        print "URL is " + str(response.url)
        
        try:
            sel = Selector(response)
        except AttributeError:
            print "   Possible redirect"
            response = urllib2.urlopen(response.url)
            if response.info()['Content-Type'] == 'application/pdf':
                print "Redirect encountered. Parse appropriately"
                return self.parse_item_from_redirect(response)
            else:
                print "BAD LINK - useless"
                return []
        
        sites = []
        for filetype in self.required_filetypes:
            sites += sel.xpath('//a[contains(@href, ".%s")]' % filetype)
        
        items = []
        for site in sites:
            item = ToolkitItem()
            
            # Get referrer
            item['referrer'] = response.url
            
            # Get link
            try:
                item['link'] = urljoin(response.url, 
                                       site.xpath('@href').extract()[0])
            except IndexError:
                item['link'] = urljoin(response.url, 
                                       site.xpath('@href').extract())
                
            # Get title
            try:
                item['title'] = site.xpath('text()').extract()[0]
            except IndexError:
                item['title'] = site.xpath('text()').extract()
            
            item['date'] = timezone.now() #datetime.now()
            items.append(item)
            
            # Save to database
            try:
                item_duplicate = DataItem.objects.get(link = item['link'],
                                                      title = item['title'])
            except DataItem.DoesNotExist:
                new_item = DataItem(spider = self.spidermodels,
                                    session = self.session,
                                    date_scraped = item['date'],
                                    link = item['link'],
                                    referrer = item['referrer'],
                                    title = item['title']) 
                new_item.save()
                return item            


        return items
    
    
    
    def parse_item_from_redirect(self, response):
        self.log('Hi, this is an item page!')
        print "Scraping a new page (FROM REDIRECT)"
        print "URL is " + str(response.url)
        
        assert(response.info()['Content-Type'] == 'application/pdf')
        
        new_title = response.info()['Content-Disposition'].split('filename=')[-1]
        new_title = new_title.replace('"','').replace("'","")
        
        url = response.url
            
        # Save to database
        try:
            item_duplicate = DataItem.objects.get(link = url,
                                                  title = new_title)
        except DataItem.DoesNotExist:
            new_item = DataItem(spider = self.spidermodels,
                                session = self.session,
                                date_scraped = timezone.now(),
                                link = url,
                                referrer = response.url,
                                title = new_title) 
            new_item.save()
            return
       
        return
                