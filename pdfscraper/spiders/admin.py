from django.contrib import admin
from spiders.models import Spider, SpiderRule, SpiderUrl, SpiderCategory


class SpiderUrlInline(admin.TabularInline):
    model = SpiderUrl

class SpiderRuleInline(admin.TabularInline):
    model = SpiderRule

class SpiderAdmin(admin.ModelAdmin): 
    search_fields=["title",]
    inlines=[SpiderRuleInline, SpiderUrlInline]
    list_display = ('title', 'is_enabled')

admin.site.register(Spider, SpiderAdmin)
admin.site.register(SpiderRule)
admin.site.register(SpiderUrl)
admin.site.register(SpiderCategory)




