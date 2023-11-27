from django.contrib import admin
from .models import Feedbacks, Contacts

class FeedbacksAdmin(admin.ModelAdmin): 
    list_display = ['name', 'phone']
    list_per_page = 10
    search_fields = ['name']
    date_hierarchy = 'created_at'


class ContactsAdmin(admin.ModelAdmin): 
    list_display = ['name', 'job', 'phone', 'email']
    list_per_page = 10
    search_fields = ['name']

admin.site.register(Feedbacks, FeedbacksAdmin)
admin.site.register(Contacts, ContactsAdmin)