from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from .models import Household, Tribe

from django.contrib.auth import get_user_model

User = get_user_model()

class HouseholdResource(resources.ModelResource):
    # user = Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, 'phone_number'))
    # year = Field(column_name='year', attribute='year', widget=ForeignKeyWidget(Tribe, 'year'))
    # tribeID = Field(column_name='tribeID', attribute='tribeID', widget=ForeignKeyWidget(Tribe, 'slug'))

    class Meta:
        model = Household
        import_id_fields = ('id',)  # Assuming 'id' is the primary key

class TribeResource(resources.ModelResource):
    user = Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, 'phone_number'))
    class Meta:
        model = Tribe
        import_id_fields = ('id',)  # Assuming 'id' is the primary key

class HouseholdAdmin(ImportExportModelAdmin):
    resource_class = HouseholdResource

class TribeAdmin(ImportExportModelAdmin):
    resource_class = TribeResource

admin.site.register(Household, HouseholdAdmin)
admin.site.register(Tribe, TribeAdmin)




