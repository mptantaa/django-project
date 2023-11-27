from django.contrib import admin
from .models import Abouts

class AboutsAdmin(admin.ModelAdmin): 
    list_display = ['title', 'about_text']
    list_per_page = 10
    search_fields = ['title']
    readonly_fields = ['title']

admin.site.register(Abouts, AboutsAdmin)