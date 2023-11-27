import json
from django.contrib import admin
from django.utils.html import format_html
from .models import History

class HistoryAdmin(admin.ModelAdmin):
    list_display = ['date', 'user', 'content_type', 'object_id']
    list_filter = ['action']
    raw_id_fields = ['user', 'content_type']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'id', 'object_id']
    list_select_related = ['user', 'content_type']
    readonly_fields = ['fields_json']



admin.site.register(History, HistoryAdmin)