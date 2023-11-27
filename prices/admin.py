from django.contrib import admin
from .models import Prices, Categories
from import_export import resources
from import_export.admin import ExportMixin, ExportActionMixin

class PricesResource(resources.ModelResource):
    class Meta:
        model = Prices
        fields = ('id', 'name', 'unit', 'price', 'category')

class PricesAdmin(ExportActionMixin, ExportMixin, admin.ModelAdmin): 
    list_display = ['name', 'unit', 'price']
    list_filter = ['unit', 'category']
    list_per_page = 10
    search_fields = ['name']
    filter_horizontal = ['category']
    resource_class = PricesResource


admin.site.register(Prices, PricesAdmin)
admin.site.register(Categories)
