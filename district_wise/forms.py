from django import forms
from .models import District

class DistrictModelForm(forms.ModelForm):
    class Meta:
        model = District
        fields = [
      
      'name',    
      'year',    
      'st_population',    
      'total_population',    
      'W_BMI',    
      'C_UW' ,   
      'AN_W',    
      'AN_C' ,   
      'AHC_ANC'  ,  
      'AHC_Full_ANC' ,   
      'AHC_PNC',    
      'AHC_HI',    
      'Enrollment',    
      'Equity',    
      'E_DropRate',    
      'S_Sani',    
      'S_CoFu',    
      'S_DrWa',    
      'S_Elec',    
        ]