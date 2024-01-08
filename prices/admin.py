from django.contrib import admin
from .models import Prices, Categories
from import_export import resources
from import_export.admin import ExportMixin, ExportActionMixin

class PricesResource(resources.ModelResource):
    class Meta:
        model = Prices
        fields = ('id', 'name', 'unit', 'price', 'category')

    def get_export_queryset(self, request):
        queryset = super().get_export_queryset(request)
        category = request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

    def dehydrate_price(self, price):
        return self.get_price(price)

    def get_price(self, price):
        return price.price * 2

class PricesAdmin(ExportActionMixin, ExportMixin, admin.ModelAdmin): 
    list_display = ['name', 'unit', 'price']
    list_filter = ['unit', 'category']
    list_per_page = 10
    search_fields = ['name']
    filter_horizontal = ['category']
    resource_class = PricesResource

admin.site.register(Prices, PricesAdmin)
admin.site.register(Categories)
