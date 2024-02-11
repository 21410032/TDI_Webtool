from django.db import models
from django.db.models import Sum
from django.core.cache import cache
from django.utils.text import slugify
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()

from django.conf import settings


# Create your models here.



class Tribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tribe',default=settings.ADMIN_USER_PHONE_NUMBER)
    year = models.IntegerField()
    name = models.CharField(max_length=50)
    Total_Sum_of_HH_S = models.IntegerField(null=True, blank=True)
    H_DI = models.FloatField(null=True, blank=True)
    E_DI = models.FloatField(null=True, blank=True)
    S_DI = models.FloatField(null=True, blank=True)
    C_DI = models.FloatField(null=True, blank=True)
    G_DI = models.FloatField(null=True, blank=True)
    tribal_incidence = models.FloatField(null=True, blank=True)
    tribal_intensity = models.FloatField(null=True, blank=True)
    TDI = models.FloatField(null=True, blank=True)
    UNC_CD_score= models.FloatField(null=True, blank=True)
    UNC_IM_score= models.FloatField(null=True, blank=True)
    UNC_MC_score= models.FloatField(null=True, blank=True)
    UNC_CM_score= models.FloatField(null=True, blank=True)
    UNC_FS_score= models.FloatField(null=True, blank=True)
    UNC_LE_score= models.FloatField(null=True, blank=True)
    UNC_DRO_score= models.FloatField(null=True, blank=True)
    UNC_IC_score= models.FloatField(null=True, blank=True)
    UNC_OW_score= models.FloatField(null=True, blank=True)
    UNC_SANI_score= models.FloatField(null=True, blank=True)
    UNC_FUEL_score= models.FloatField(null=True, blank=True)
    UNC_DRWA_score= models.FloatField(null=True, blank=True)
    UNC_ELECTR_score= models.FloatField(null=True, blank=True)
    UNC_ASS_score= models.FloatField(null=True, blank=True)
    UNC_LAN_score= models.FloatField(null=True, blank=True)
    UNC_ARTS_score= models.FloatField(null=True, blank=True)
    UNC_EV_score= models.FloatField(null=True, blank=True)
    UNC_MEET_score= models.FloatField(null=True, blank=True)

    CEN_CD_score= models.FloatField(null=True, blank=True)
    CEN_IM_score= models.FloatField(null=True, blank=True)
    CEN_MC_score= models.FloatField(null=True, blank=True)
    CEN_CM_score= models.FloatField(null=True, blank=True)
    CEN_FS_score= models.FloatField(null=True, blank=True)
    CEN_LE_score= models.FloatField(null=True, blank=True)
    CEN_DRO_score= models.FloatField(null=True, blank=True)
    CEN_IC_score= models.FloatField(null=True, blank=True)
    CEN_OW_score= models.FloatField(null=True, blank=True)
    CEN_SANI_score= models.FloatField(null=True, blank=True)
    CEN_FUEL_score= models.FloatField(null=True, blank=True)
    CEN_DRWA_score= models.FloatField(null=True, blank=True)
    CEN_ELECTR_score= models.FloatField(null=True, blank=True)
    CEN_ASS_score= models.FloatField(null=True, blank=True)
    CEN_LAN_score= models.FloatField(null=True, blank=True)
    CEN_ARTS_score= models.FloatField(null=True, blank=True)
    CEN_EV_score= models.FloatField(null=True, blank=True)
    CEN_MEET_score= models.FloatField(null=True, blank=True)
    village_details = models.JSONField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'year', 'name')


    def save(self, *args, **kwargs):
        # self.slug = slugify(self.name)
        super(Tribe, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}-{self.year}-{self.id}"
    
