from django.contrib import admin
from dataitems.models import DataItem

class DataItemAdmin(admin.ModelAdmin): 
    search_fields=["title","spider", "link"]
    list_display = ('title', 'filename', 'date_scraped', 'spider')
admin.site.register(DataItem, DataItemAdmin)



