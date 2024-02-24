from django import forms
from .models import Tribe


class TribeForm(forms.ModelForm):

    class Meta:
        model = Tribe
        fields = [
            'user',
            'year',
            'name',
            'total_tribals',
            'H_DI',
            'E_DI',
            'S_DI',
            'C_DI',
            'G_DI',
            'tribal_incidence',
            'tribal_intensity',
            'TDI',
            'UNC_CD_score',
            'UNC_IM_score',
            'UNC_MC_score',
            'UNC_CM_score',
            'UNC_FS_score',
            'UNC_LE_score',
            'UNC_DRO_score',
            'UNC_IC_score',
            'UNC_OW_score',
            'UNC_SANI_score',
            'UNC_FUEL_score',
            'UNC_DRWA_score',
            'UNC_ELECTR_score',
            'UNC_ASS_score',
            'UNC_LAN_score',
            'UNC_ARTS_score',
            'UNC_EV_score',
            'UNC_MEET_score',
            'CEN_CD_score',
            'CEN_IM_score',
            'CEN_MC_score',
            'CEN_CM_score',
            'CEN_FS_score',
            'CEN_LE_score',
            'CEN_DRO_score',
            'CEN_IC_score',
            'CEN_OW_score',
            'CEN_SANI_score',
            'CEN_FUEL_score',
            'CEN_DRWA_score',
            'CEN_ELECTR_score',
            'CEN_ASS_score',
            'CEN_LAN_score',
            'CEN_ARTS_score',
            'CEN_EV_score',
            'CEN_MEET_score',
            'CD_contri_to_H',
            'IM_contri_to_H',
            'MC_contri_to_H',
            'CM_contri_to_H',
            'FS_contri_to_H',

            'LE_contri_to_E',
            'DRO_contri_to_E',

            'IC_contri_to_S',
            'OW_contri_to_S',
            'SANI_contri_to_S',
            'FUEL_contri_to_S',
            'DRWA_contri_to_S',
            'ELECTR_contri_to_S',
            'ASS_contri_to_S',

            'LAN_contri_to_C',
            'ARTS_contri_to_C',

            'EV_contri_to_G',
            'MEET_contri_to_G',

            'H_contri_to_TDI',
            'E_contri_to_TDI',
            'S_contri_to_TDI',
            'C_contri_to_TDI',
            'G_contri_to_TDI',
        ]