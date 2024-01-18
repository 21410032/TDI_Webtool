from django import forms
from .models import Household

class HouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = [
            'tribeID',
            'size',
            'CD_score',   
            'IM_score',   
            'MC_score',   
            'CM_score',   
            'FS_score',   
            'LE_score',   
            'DRO_score', 
            'IC_score',  
            'OW_score',  
            'SANI_score',  
            'FUEL_score',  
            'DRWA_score',  
            'ELECTR_score',
            'ASS_score', 
            'LAN_score', 
            'ARTS_score', 
            'EV_score',  
            'MEET_score'  
        ]
        