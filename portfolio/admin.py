from django.contrib import admin
from django.db import models
from .models import Portlofios
from import_export import resources
from import_export.admin import ExportMixin, ExportActionMixin

class PortlofiosResource(resources.ModelResource):

    class Meta:
        model = Portlofios
        fields = ('id', 'name', 'unit', 'description', 'image')


class PortlofiosAdmin(ExportActionMixin, ExportMixin, admin.ModelAdmin):
    list_display = ['name', 'unit', 'image']
    list_per_page = 10
    search_fields = ['name']
    formfield_overrides = {
        models.ImageField: {'widget': admin.widgets.AdminFileWidget},
    }
    resource_class = PortlofiosResource


admin.site.register(Portlofios, PortlofiosAdmin)
