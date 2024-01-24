from import_export import resources
from .models import Tribe, Household, Tribe_Image

class HouseholdResource(resources.ModelResource):
    class meta:
        model = Household