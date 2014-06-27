# Scrapy settings for toolkit project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'toolkit'

SPIDER_MODULES = ['toolkit.spiders']
NEWSPIDER_MODULE = 'toolkit.spiders'

ITEM_PIPELINES = {
    'toolkit.toolkit.pipelines.DbInsertPipeline': 300,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'toolkit (+http://www.yourdomain.com)'
