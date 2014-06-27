from django.contrib import admin
from scrapesessions.models import SpiderSession




class SpiderSessionAdmin(admin.ModelAdmin): 
    search_fields=["id",]
    list_display = ('id', 'time_started', 'time_ended', 'total_time')

admin.site.register(SpiderSession, SpiderSessionAdmin)





