from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
# Register your models here.

class ViewAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    pass

admin.site.register(District, ViewAdmin)




