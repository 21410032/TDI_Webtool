from django.contrib import admin
# Register your models here.
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
# Register your models here.

admin.site.register(Tribe_Image)


class ViewAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    pass



admin.site.register(Household, ViewAdmin)
# class HouseholdAdmin(ImportExportModelAdmin):
#     list_display = ['size', 'tribe']

admin.site.register(Tribe, ViewAdmin)
# class TribeAdmin(admin.ModelAdmin):
#     list_display = [ 'name']



