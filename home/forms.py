from django import forms
from .models import Household

class HouseholdForm(forms.ModelForm):

    tribe_choices = [
    ('kawar', 'Kawar'),
    ('baiga', 'Baiga'),
    ('gorait', 'Gorait'),
    ('kol', 'Kol'),
    ('karmali', 'Karmali'),
    ('chik_baraik', 'Chik Baraik'),
    ('kisan', 'Kisan'),
    ('kora', 'Kora'),
    ('gond', 'Gond'),
    ('Binjhia', 'Binjhia'),
    ('Chero', 'Chero'),
    ('Mehli', 'Mehli'),
    ('Santal', 'Santal'),
    ('Oraon', 'Oraon'),
    ('Kharia', 'Kharia'),
    ('munda', 'Munda'),
    ('kharwar', 'Kharwar'),
    ('bhumij', 'Bhumij'),
    ('bedia', 'Bedia'),
    ('lohra', 'Lohra'),
    ('ho', 'Ho'),
    ('sauria_parhaiya', 'Sauria Parhaiya'),
    ('savar', 'Savar'),
    ('parhiya', 'Parhiya'),
    ('mal_paharia', 'Mal Paharia'),
    ('korwa', 'Korwa'),
    ('birjia', 'Birjia'),
    ('birhor', 'Birhor'),
    ('asur', 'Asur'),
]



    tribe_slug = forms.ChoiceField(choices=tribe_choices, required=True, label='Tribe')
    class Meta:
        model = Household
        fields = [
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

