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
    incidence = models.FloatField(null=True, blank=True)
    intensity = models.FloatField(null=True, blank=True)
    tdi = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'year', 'name')

    
    


    def save(self, *args, **kwargs):
        # self.slug = slugify(self.name)
        super(Tribe, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}-{self.year}-{self.id}"
    

    @property
    def get_total_tribals(self):
        if hasattr(self, '_get_total_tribals'):
            return self._get_total_tribals

        total_tribals = self.household.aggregate(total_tribals=Sum('size'))['total_tribals']
        self._get_total_tribals = total_tribals or 0
        return self._get_total_tribals


    @property
    def total_members_across_onedimensionally_developed_households(self):
        if hasattr(self, '_total_members_onedimensionally_developed'):
            return self._total_members_onedimensionally_developed

        ans = [0] * 5
        households = self.household.all()

        for household in households:
            is_developed = household.is_developed
            for i in range(5):
                ans[i] += is_developed[i] * household.size

        self._total_members_onedimensionally_developed = ans
        return ans
    


    @property
    def total_households_across_onedindicator_developed_households(self):
        if hasattr(self, '_total_households_onedindicator_developed'):
            return self._total_households_onedindicator_developed

        ans = [0] * 5
        households = self.household.all()

        for household in households:
            is_developed = household.is_developed
            for i in range(5):
                ans[i] += is_developed[i]

        self._total_households_onedindicator_developed = ans
        return ans

    

    @property
    def dimensional_contribution_to_index(self):
        if not hasattr(self, '_dimensional_contribution_to_index'):
            self._dimensional_contribution_to_index = self._calculate_dimensional_contribution_to_index()
        return self._dimensional_contribution_to_index

    @property
    def tribal_dimensional_incidence(self):
        if not hasattr(self, '_tribal_dimensional_incidence'):
            self._tribal_dimensional_incidence = self._calculate_tribal_dimensional_incidence()
        return self._tribal_dimensional_incidence

    @property
    def tribal_incidence(self):
        if not hasattr(self, '_tribal_incidence'):
            self._tribal_incidence = self._calculate_tribal_incidence()
        return self._tribal_incidence

    @property
    def tribal_dimensional_intensity(self):
        if not hasattr(self, '_tribal_dimensional_intensity'):
            self._tribal_dimensional_intensity = self._calculate_tribal_dimensional_intensity()
        return self._tribal_dimensional_intensity

    def _calculate_dimensional_contribution_to_index(self):
        tribe_households = self.household.all()
        total_tribals = self.get_total_tribals
        
        ans = [0] * 5
        
        for household in tribe_households:
            members_of_developed_households = household.members_of_developed_households
            for i in range(5):
                ans[i] += members_of_developed_households[i]
        
        dimensional_contribution_to_index = [i / total_tribals for i in ans if total_tribals != 0]
        # Round off the values in the list to 2 decimal places
        rounded_dimensional_contribution = [round(value, 2) for value in dimensional_contribution_to_index]
        
        return rounded_dimensional_contribution

    def _calculate_tribal_dimensional_incidence(self):
        ans = [0] * 5
        households = self.household.all()

        for i in range(5):
            for household in households:
                ans[i] += household.household_dimensional_incidence[i]

        ans = [round(val, 4) for val in ans]

        return ans

    def _calculate_tribal_incidence(self):
        ans = 0
        tribe_households = self.household.all()

        for household in tribe_households:
            household_tribal_incidence = household.household_tribal_incidence
            ans += household_tribal_incidence

        return int(round(ans * 100, 3))

    def _calculate_tribal_dimensional_intensity(self):
        ans = [0] * 5
        households = self.household.all()

        for i in range(5):
            for household in households:
                ans[i] += household.household_dimensional_intensity[i]

        ans = [round(val, 3) for val in ans]

        return ans
    

    @property
    def tribal_intensity(self):
        if not hasattr(self, '_tribal_intensity'):
            self._tribal_intensity = self._calculate_tribal_intensity()
        return self._tribal_intensity

    @property
    def tribal_dimensional_index(self):
        if not hasattr(self, '_tribal_dimensional_index'):
            self._tribal_dimensional_index = self._calculate_tribal_dimensional_index()
        return self._tribal_dimensional_index

    @property
    def tribal_index(self):
        if not hasattr(self, '_tribal_index'):
            self._tribal_index = self._calculate_tribal_index()
        return self._tribal_index

    @property
    def total_members_multi_dimensionally_developed_households(self):
        if not hasattr(self, '_total_members_multi_dimensionally_developed_households'):
            self._total_members_multi_dimensionally_developed_households = self._calculate_total_members_multi_dimensionally_developed_households()
        return self._total_members_multi_dimensionally_developed_households

    @property
    def indicators_score(self):
        if not hasattr(self, '_indicators_score'):
            self._indicators_score = self._calculate_indicators_score()
        return self._indicators_score

    @property
    def dimensional_score(self):
        if not hasattr(self, '_dimensional_score'):
            self._dimensional_score = self._calculate_dimensional_score()
        return self._dimensional_score

    @property
    def indicator_contributions_to_dimension(self):
        if not hasattr(self, '_indicator_contributions_to_dimension'):
            self._indicator_contributions_to_dimension = self._calculate_indicator_contributions_to_dimension()
        return self._indicator_contributions_to_dimension

    @property
    def dimension_contribution_to_tdi(self):
        if not hasattr(self, '_dimension_contribution_to_tdi'):
            self._dimension_contribution_to_tdi = self._calculate_dimension_contribution_to_tdi()
        return self._dimension_contribution_to_tdi
    


    def _calculate_tribal_intensity(self):
        households = self.household.all()
        cnt = 0
        for household in households:
            household_tribal_intensity = household.household_tribal_intensity
            cnt += household_tribal_intensity
        return int(round(cnt * 100, 2))

    def _calculate_tribal_dimensional_index(self):
        incidence_values = self.tribal_dimensional_incidence
        intensity_values = self.tribal_dimensional_intensity

        ans = [round(incidence_values[i] * intensity_values[i], 3) for i in range(5)]

        return ans

    def _calculate_tribal_index(self):
        tribal_incidence = self.tribal_incidence / 100
        tribal_intensity = self.tribal_intensity / 100
        tribal_index = tribal_incidence * tribal_intensity
        return round(tribal_index, 2)

    def _calculate_total_members_multi_dimensionally_developed_households(self):
        households = self.household.all()
        total_members = 0

        for household in households:
            if household.is_multidimensionally_developed:
                total_members += household.size

        return total_members

    def _calculate_indicators_score(self):
        households = self.household.all()
        total = []

        if households:
            # Initialize the 'total' list with the test indicators of the first household
            total = [[0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]

            for household in households:
                indicators = household.test_indicators
                for i in range(len(indicators)):
                    for j in range(len(indicators[i])):
                        if indicators[i][j] is not None:
                            total[i][j] += indicators[i][j]

        return total



    def _calculate_dimensional_score(self):
        households = self.household.all()
        ans = [0] * 5

        for i in range(5):
            for household in households:
                D_ds = household.D_DS[i]
                if D_ds:
                    ans[i] += D_ds

        return ans

    def _calculate_indicator_contributions_to_dimension(self):
        dimensional_scores = self.dimensional_score
        indicator_scores = self.indicators_score
        contributions = []

        for i in range(len(indicator_scores)):
            if dimensional_scores[i] != 0:
                indicator_contribution = [
                    round((score / dimensional_scores[i]) * 100, 2) for score in indicator_scores[i]
                ]
                contributions.append(indicator_contribution)

        return contributions

    def _calculate_dimension_contribution_to_tdi(self):
        households = self.household.all()
        dimension_contribution_to_tdi = []
        total_D_DS = [0] * 5
        total_tribal_development_score = 0

        for i in range(5):
            for household in households:
                D_DS = household.D_DS[i]
                total_D_DS[i] += D_DS

        for household in households:
            tribal_development_score = household.tribal_development_score
            total_tribal_development_score += tribal_development_score

        if total_tribal_development_score != 0:
            dimension_contribution_to_tdi = [round((i / total_tribal_development_score) * 100, 2) for i in total_D_DS]
        return dimension_contribution_to_tdi

        


 
    @property
    def get_censored_tribal_indicator_score(self):
        cache_key = 'censored_tribal_indicator_score_' + str(self.id)
        cached_value = cache.get(cache_key)

        if cached_value is not None:
            return cached_value

        households = self.household.all()
        scores = {
            'CD_score':    0,
            'IM_score':    0,
            'MC_score':    0,
            'CM_score':    0,
            'FS_score':    0,
            'LE_score':    0,
            'DRO_score':    0,
            'IC_score':    0,
            'OW_score':    0,
            'SANI_score'   : 0,
            'FUEL_score'   : 0,
            'DRWA_score'   : 0,
            'ELECTR_score': 0,
            'ASS_score':    0,
            'LAN_score':    0,
            'ARTS_score'   : 0,
            'EV_score':    0,
            'MEET_score'   : 0
        }

        total_members = self.get_total_tribals

        for household in households:
                tribal_development_score = household.tribal_development_score

                if tribal_development_score > 0.33:
                    for key in scores:
                        score = getattr(household, key)
                        scores[key] += score * household.size if score is not None else 0

        if total_members > 0:
                ans = [round(scores[key] / total_members, 2) for key in scores]
        else:
            ans = []
            error_message = "Number of household members cannot be zero"
            raise ValueError(error_message)  # Set ans to an empty list or another appropriate value when total_members is zero
        return ans
            


        
    @property
    def get_uncensored_tribal_indicator_score(self):
        cache_key = 'uncensored_tribal_indicator_score_' + str(self.id)
        cached_value = cache.get(cache_key)

        if cached_value is not None:
            return cached_value

        households = self.household.all()
        scores = {
            'CD_score': 0,
            'IM_score': 0,
            'MC_score': 0,
            'CM_score': 0,
            'FS_score': 0,
            'LE_score': 0,
            'DRO_score': 0,
            'IC_score': 0,
            'OW_score': 0,
            'SANI_score': 0,
            'FUEL_score': 0,
            'DRWA_score': 0,
            'ELECTR_score': 0,
            'ASS_score': 0,
            'LAN_score': 0,
            'ARTS_score': 0,
            'EV_score': 0,
            'MEET_score': 0
        }

        total_members = self.get_total_tribals

        for household in households:
            for key in scores:
                score = getattr(household, key)
                scores[key] += score * household.size if score is not None else 0

        ans = [round(scores[key] / total_members, 2) for key in scores]

        cache.set(cache_key, ans)
        return ans




class Tribe_Image(models.Model):
    tribe = models.ForeignKey(Tribe, on_delete=models.CASCADE, related_name='tribe_image', null=True, blank=True)
    logo_image=models.ImageField(upload_to='images/logo_images')
    main_image=models.ImageField(upload_to='images/main_images')
    main_desc = models.CharField(max_length=100,null=True, blank=True)
    village_image=models.ImageField(upload_to='images/village_images')
    village_desc = models.CharField(max_length=100,null=True, blank=True)
    location=models.CharField(max_length=50, null=True, blank=True)
    map_image = models.ImageField(upload_to='images/map_images')
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.tribe.name} images"


class Household(models.Model):
    tribeID = models.ForeignKey(Tribe, on_delete=models.CASCADE, related_name="household", null=True)
    size = models.IntegerField(null= True)
    
    # HEALTH
    CD_score = models.BooleanField(null = True, blank=True)
    IM_score = models.BooleanField(null = True, blank=True)
    MC_score = models.BooleanField(null = True, blank=True)

    CM_score = models.BooleanField(null = True, blank=True)
    FS_score = models.BooleanField(null = True, blank=True)

    # EDUCATION
    LE_score = models.BooleanField(null = True, blank=True)
    DRO_score = models.BooleanField(null = True, blank=True)

    #SOL
    IC_score = models.BooleanField(null = True, blank=True)
    OW_score = models.BooleanField(null = True, blank=True)
    SANI_score = models.BooleanField(null = True, blank=True)
    FUEL_score = models.BooleanField(null = True, blank=True)
    DRWA_score = models.BooleanField(null = True, blank=True)
    ELECTR_score = models.BooleanField(null = True, blank=True)
    ASS_score = models.BooleanField(null = True, blank=True)

    #CULTURE
    LAN_score = models.BooleanField(null = True, blank=True)
    ARTS_score = models.BooleanField(null = True, blank=True)

    #GOVERNANCE
    EV_score = models.BooleanField(null = True, blank=True)
    MEET_score = models.BooleanField(null = True, blank=True)
 
    
    def __str__(self):
        return f"HH ({self.tribeID.name})-{self.tribeID.year}-{self.size}"




    @property
    def no_of_indicators(self):
        if hasattr(self, '_cached_no_of_indicators'):
            return self._cached_no_of_indicators

        scores_H = [self.CD_score, self.IM_score, self.MC_score, self.CM_score, self.FS_score]
        scores_E = [self.LE_score, self.DRO_score]
        scores_S = [self.IC_score, self.OW_score, self.SANI_score, self.FUEL_score, self.DRWA_score, self.ELECTR_score, self.ASS_score]
        scores_C = [self.LAN_score, self.ARTS_score]
        scores_G = [self.EV_score, self.MEET_score]

        scores = [scores_H, scores_E, scores_S, scores_C, scores_G]

        ans = [sum(1 for score in sublist if score is not None) for sublist in scores]

        self._cached_no_of_indicators = ans
        return ans

    @property
    def developed_indicators(self):
        if hasattr(self, '_cached_developed_indicators'):
            return self._cached_developed_indicators

        scores_H = [self.CD_score, self.IM_score, self.MC_score, self.CM_score, self.FS_score]
        scores_E = [self.LE_score, self.DRO_score]
        scores_S = [self.IC_score, self.OW_score, self.SANI_score, self.FUEL_score, self.DRWA_score, self.ELECTR_score, self.ASS_score]
        scores_C = [self.LAN_score, self.ARTS_score]
        scores_G = [self.EV_score, self.MEET_score]

        scores = [scores_H, scores_E, scores_S, scores_C, scores_G]

        ans = [sum(score for score in sublist if score is not None) for sublist in scores]

        self._cached_developed_indicators = ans
        return ans


    @property
    def calculate_weightage(self):
        if hasattr(self, '_cached_weightage'):
            return self._cached_weightage

        no_of_indicators = self.no_of_indicators
        ans = [round(0.2 * (1 / no) if no else 0, 2) for no in no_of_indicators]

        self._cached_weightage = ans
        return ans

    @property
    def test_indicators(self):
        if hasattr(self, '_cached_test_indicators'):
            return self._cached_test_indicators

        scores_H = [self.CD_score, self.IM_score, self.MC_score, self.CM_score, self.FS_score]
        scores_E = [self.LE_score, self.DRO_score]
        scores_S = [self.IC_score, self.OW_score, self.SANI_score, self.FUEL_score, self.DRWA_score, self.ELECTR_score, self.ASS_score]
        scores_C = [self.LAN_score, self.ARTS_score]
        scores_G = [self.EV_score, self.MEET_score]

        weightage = self.calculate_weightage
        scores = [scores_H, scores_E, scores_S, scores_C, scores_G]
        ans = []

        for i in range(0,5):
            dimension_indicators_array = []
            for j in scores[i]:
                if j is not None:
                    dimension_indicators_array.append(round(j * weightage[i], 2))
                else:
                    dimension_indicators_array.append(None)  # Append None if j is None
            ans.append(dimension_indicators_array)

        self._cached_test_indicators = ans
        return ans


    @property
    def D_DS(self):
        if hasattr(self, '_cached_D_DS'):
            return self._cached_D_DS

        weightage = self.calculate_weightage
        developed_indicators = self.developed_indicators
        ans = [w * d for w, d in zip(weightage, developed_indicators)]

        self._cached_D_DS = ans
        return ans

    @property
    def is_developed(self):
        if hasattr(self, '_cached_is_developed'):
            return self._cached_is_developed

        D_DS = self.D_DS
        ans = [1 if d_ds >= 0.066 else 0 for d_ds in D_DS]

        self._cached_is_developed = ans
        return ans

    
    @property
    def tribal_development_score(self):
        if hasattr(self, '_cached_tribal_development_score'):
            return self._cached_tribal_development_score

        score = round(sum(self.D_DS), 2)
        self._cached_tribal_development_score = score
        return score

    @property
    def is_multidimensionally_developed(self):
        if hasattr(self, '_cached_is_multidimensionally_developed'):
            return self._cached_is_multidimensionally_developed

        is_dev = self.is_developed
        score = 1 if self.tribal_development_score > 0.33 else 0
        self._cached_is_multidimensionally_developed = score
        return score

    @property
    def members_of_developed_households(self):
        if hasattr(self, '_cached_members_of_developed_households'):
            return self._cached_members_of_developed_households

        is_dev = self.is_developed
        members = [is_dev[i] * self.size for i in range(5)]
        self._cached_members_of_developed_households = members
        return members

    @property
    def household_dimensional_incidence(self):
        if hasattr(self, '_cached_household_dimensional_incidence'):
            return self._cached_household_dimensional_incidence

        total_tribals = self.tribeID.get_total_tribals
        incidence = []

        members_of_developed_households = self.members_of_developed_households  # Calculate once

        for i in range(5):
            if total_tribals > 0:
                incidence_value = members_of_developed_households[i] / total_tribals
            else:
                incidence_value = 0.0  # Handle the case where there are no households to avoid division by zero
            round(incidence_value,2)
            incidence.append(incidence_value)

        self._cached_household_dimensional_incidence = incidence
        return incidence

    
    @property
    def household_tribal_incidence(self):
        if hasattr(self, '_cached_household_tribal_incidence'):
            return self._cached_household_tribal_incidence

        total_tribals = self.tribeID.get_total_tribals
        is_multidimensionally_developed = self.is_multidimensionally_developed

        if total_tribals > 0:
            ans = (is_multidimensionally_developed * self.size) / total_tribals
        else:
            ans = 0.0  # Handle the case where there are no tribals to avoid division by zero
        self._cached_household_tribal_incidence = ans
        return round(ans,2)

    @property
    def household_dimensional_intensity(self):
        if hasattr(self, '_cached_household_dimensional_intensity'):
            return self._cached_household_dimensional_intensity

        intensity = []

        # Calculate the shared values once before the loop
        total_members_across_onedimensionally_developed_households = self.tribeID.total_members_across_onedimensionally_developed_households
        members_in_developed_households = self.members_of_developed_households
        D_DS_values = self.D_DS

        for i in range(0, 5):
            total_members = total_members_across_onedimensionally_developed_households[i]
            members_in_households = members_in_developed_households[i]
            score = D_DS_values[i]

            if total_members > 0:
                ans = (score * members_in_households * 5) / total_members
            else:
                ans = 0.0  # Handle the case where total_members is zero
            round(ans)
            intensity.append(ans)

        self._cached_household_dimensional_intensity = intensity
        return intensity

    @property
    def household_tribal_intensity(self):
        if hasattr(self, '_cached_household_tribal_intensity'):
            return self._cached_household_tribal_intensity

        # Calculate the shared values once before the loop
        total_members_multi_dimensionally_developed_households = self.tribeID.total_members_multi_dimensionally_developed_households
        members_in_developed_households = self.size if self.is_multidimensionally_developed else 0
        score = self.tribal_development_score

        if total_members_multi_dimensionally_developed_households > 0:
            ans = (score * members_in_developed_households) / total_members_multi_dimensionally_developed_households
        else:
            ans = 0.0  # Handle the case where total_members_multi_dimensionally_developed_households is zero

        self._cached_household_tribal_intensity = ans
        return round(ans,2)

    @property
    def household_tribal_index(self):
        if hasattr(self, '_cached_household_tribal_index'):
            return self._cached_household_tribal_index

        household_tribal_intensity = self.household_tribal_intensity
        household_tribal_incidence = self.household_tribal_incidence
        index = round((household_tribal_intensity * household_tribal_incidence) * 100, 5)

        self._cached_household_tribal_index = index
        return index

    @property
    def developed_indicators_members(self):
        if hasattr(self, '_cached_developed_indicators_members'):
            return self._cached_developed_indicators_members

        scores_H = [self.CD_score, self.IM_score, self.MC_score, self.CM_score, self.FS_score]
        scores_E = [self.LE_score, self.DRO_score]
        scores_S = [self.IC_score, self.OW_score, self.SANI_score, self.FUEL_score, self.DRWA_score, self.ELECTR_score, self.ASS_score]
        scores_C = [self.LAN_score, self.ARTS_score]
        scores_G = [self.EV_score, self.MEET_score]

        scores = [scores_H, scores_E, scores_S, scores_C, scores_G]
        total_sum = 0

        for indicator_group in scores:
            total_sum += sum([score for score in indicator_group if score is not None])

        result = round(total_sum * self.size, 4)

        self._cached_developed_indicators_members = result
        return result



class User_Hitcounts(models.Model):
    site_views = models.IntegerField(default=0)
    last_refresh_time = models.DateTimeField(null=True, blank=True)

    @classmethod
    def get_site_views(cls):
        # This method returns the total site views
        instance, created = cls.objects.get_or_create(pk=1)
        return instance.site_views

    @classmethod
    def increment_site_views(cls):
        # This method increments the total site views
        instance, created = cls.objects.get_or_create(pk=1)
        if instance.last_refresh_time is None or (timezone.now() - instance.last_refresh_time).total_seconds() > 600:  # 300 seconds = 10 minutes
            instance.site_views += 1
            instance.last_refresh_time = timezone.now()
            instance.save()
        return instance.site_views