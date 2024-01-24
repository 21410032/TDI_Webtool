from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from import_export import resources, fields
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from .models import Household, Tribe
from accounts.models import Profile
from .resources import HouseholdResource
from django.contrib.auth import get_user_model

User = get_user_model()

# class HouseholdResource(resources.ModelResource):
#     def get_tribeID(self, row, **kwargs):
#         user_phone_number = row.get('user')
#         year = row.get('year')
#         slug = row.get('tribeID')
#         user = Profile.objects.get(phone_number = user_phone_number)
#         print(f"user_phone_number: {user_phone_number}, year: {year}, slug: {slug}")
#         try:
#             print('********')
#             tribe, created = Tribe.objects.get_or_create(user=user, year=year, slug=slug)
#             print(tribe)
#             print('********')
#             row['tribeID'] = tribe.id
#             print(tribe.id)
#         except Tribe.DoesNotExist:
#             print("Tribe does not exist")
#             print('-8-8-8-8-88')

#         return row  # Return the modified row

    
#     tribeID = fields.Field(
#         column_name='tribeID',
#         attribute= self.get_tribeID,
#         widget=ForeignKeyWidget(Tribe, 'slug')  # Assuming 'slug' is a unique field of Tribe model
#     )
#     user = fields.Field(
#         column_name='user',
#         attribute='tribeID__user__phone_number',
#         widget=ForeignKeyWidget(User, 'phone_number')
#     )
#     year = fields.Field(
#         column_name='year',
#         attribute='tribeID__year',
#         widget=ForeignKeyWidget(Tribe, 'year')
#     )

#     class Meta:
#         model = Household
#         fields = ('tribeID', 'size', 'user', 'year')  # Specify the fields to import/export
#         import_id_fields = ('tribeID',)  # Specify the import id fields


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




