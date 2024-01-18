from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import Http404
from .models import Household, Tribe,Tribe_Image
from district_wise.models import District
from django.http import HttpResponse
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
from .forms import HouseholdForm
from django.forms import formset_factory



def tribe_detail_view(request, slug, year):


    user_phone_number = request.GET.get('user')
    if user_phone_number:
        user = User.objects.get(phone_number=user_phone_number)

    else:    
        user = User.objects.get(phone_number='7219142469')

    tribes = Tribe.objects.filter(household__user=user, household__year='2022').distinct()

    if slug and year is not None:
        try:
            tribe = Tribe.objects.get(household__user=user, slug=slug, household__year=year)
        except Tribe.DoesNotExist:
            raise Http404
        except:
            raise Http404

    total_tribals = tribe.get_total_tribals
    household = Household.objects.all()
    districts = District.objects.all()
    
    contributions_to_dimension = tribe.indicator_contributions_to_dimension

    health_contributions_to_dimension = contributions_to_dimension[0] if contributions_to_dimension and len(contributions_to_dimension) > 0 else None
    education_contributions_to_dimension = contributions_to_dimension[1] if contributions_to_dimension and len(contributions_to_dimension) > 1 else None
    sol_contributions_to_dimension = contributions_to_dimension[2] if contributions_to_dimension and len(contributions_to_dimension) > 2 else None
    culture_contributions_to_dimension = contributions_to_dimension[3] if contributions_to_dimension and len(contributions_to_dimension) > 3 else None
    governance_contributions_to_dimension = contributions_to_dimension[4] if contributions_to_dimension and len(contributions_to_dimension) > 4 else None

    tribal_dimensional_index = tribe.tribal_dimensional_index
    dimension_contribution_to_tdi = tribe.dimension_contribution_to_tdi

    
    
    context = {
        'household': household,
        'total_tribals': total_tribals,
        'tribe': tribe,
        'tribes' : tribes,
        'health_contributions_to_dimension': health_contributions_to_dimension,
        'education_contributions_to_dimension': education_contributions_to_dimension,
        'sol_contributions_to_dimension': sol_contributions_to_dimension,
        'culture_contributions_to_dimension': culture_contributions_to_dimension,
        'governance_contributions_to_dimension': governance_contributions_to_dimension,
        'tribal_dimensional_index': tribal_dimensional_index,
        'dimension_contribution_to_tdi': dimension_contribution_to_tdi,
        'districts' : districts,
    }
        


    return render(request, 'pvtg/asur.html', context=context)


# def asur_view(request):
     

#      health=Health.objects.all()
#      education=Education.objects.all()
#      sol=SOL.objects.all()
#      culture=Culture.objects.all()
#      governance=Governance.objects.all()
#      health_incidence=0
#      health_intensity=0
#      education_incidence=0
#      education_intensity=0
#      sol_incidence=0
#      sol_intensity=0
#      culture_incidence=0
#      culture_intensity=0
#      governance_incidence=0
#      governance_intensity=0
#      for i in health:
#         health_incidence+=i.H_incidence
#         health_intensity+=i.H_intensity
#      for i in education:
#         education_incidence+=i.E_incidence
#         education_intensity+=i.E_intensity
#      for i in sol:
#         sol_incidence+=i.S_incidence
#         sol_intensity+=i.S_intensity
#      for i in culture:
#         culture_intensity+=i.C_incidence
#         culture_incidence+=i.C_intensity
#      for i in governance:
#         governance_incidence+=i.G_incidence
#         governance_intensity+=i.G_intensity

#         # print(health_incidence)
        
#         # print(health_intensity)
      
#      health_index=round((health_incidence*health_intensity),2)
#      education_index=round((education_incidence*education_intensity),2)
#      sol_index=round((sol_incidence*sol_intensity),2)
#      culture_index=round((culture_incidence*culture_intensity),2)
#      governance_index=round((governance_incidence*governance_intensity),2)

#      HH_dimension_dev_score = health.score + education.score + sol.score  + culture.score  + governance.score
     
     
#      context={
#          'health':health,
#          'education':education,
#           "sol":sol,
#           'culture':culture,
#           'governance':governance,
#           'health_index':health_index,
#           'education_index':education_index,
#           'sol_index':sol_index,
#           'culture_index':culture_index,
#           'governance_index':governance_index
          
           
#      }
#      return render(request,'pvtg/asur.html',context=context)


def test_view(request):
    
    tribe = Tribe.objects.get(id = 2)
    total_tribals = tribe.get_total_tribals
    household = Household.objects.all()
    
    
    
    context = {
        'household' : household,
        'total_tribals' : total_tribals,
        'tribe' : tribe,
        

    }
    return render(request, 'pvtg/test.html', context)

def form_view(request):
    YourModelFormSet = formset_factory(HouseholdForm, extra=1, can_delete=True, validate_max=True)
    user = User.objects.get(phone_number='7219142469')
    tribes = Tribe.objects.filter(household__user=user, household__year='2022').distinct()

    if request.method == 'POST':
        formset = YourModelFormSet(request.POST, prefix='form')
        cleaned_data_list = []
        # Set the initial year for each form
    
        year = request.POST.get('year')

        user_from_form = request.user if request.user.is_authenticated else user

        for form in formset:
            if form.is_valid():
  
            
                tribeID = form.cleaned_data['tribeID']
                tribe, created = Tribe.objects.get_or_create(slug=tribeID)

                household = form.save(commit=False)
                household.user = user_from_form
                household.tribe = tribe
                household.year = year
                household.save()
                cleaned_data_list.append(form.cleaned_data)

        if cleaned_data_list:
            redirect_url = f'/tribe/asur/{request.POST["year"]}?user={user_from_form.phone_number}'
            return redirect(redirect_url)
        else:
            # Print form errors to understand why validation failed
            for form in formset:
                print(form.errors)

    else:
        formset = YourModelFormSet(prefix='form')

    return render(request, 'form/form.html', {'formset': formset, 'tribes': tribes})

    
    

    
def tribe_pdf_view(request, slug):
    tribe = Tribe.objects.get(slug = slug)
    tribes = Tribe.objects.all()
    user = request.user

    total_tribals = tribe.get_total_tribals
    household = Household.objects.all()
    districts = District.objects.all()
    
    contributions_to_dimension = tribe.indicator_contributions_to_dimension

    health_contributions_to_dimension = contributions_to_dimension[0] if contributions_to_dimension and len(contributions_to_dimension) > 0 else None
    education_contributions_to_dimension = contributions_to_dimension[1] if contributions_to_dimension and len(contributions_to_dimension) > 1 else None
    sol_contributions_to_dimension = contributions_to_dimension[2] if contributions_to_dimension and len(contributions_to_dimension) > 2 else None
    culture_contributions_to_dimension = contributions_to_dimension[3] if contributions_to_dimension and len(contributions_to_dimension) > 3 else None
    governance_contributions_to_dimension = contributions_to_dimension[4] if contributions_to_dimension and len(contributions_to_dimension) > 4 else None

    tribal_dimensional_index = tribe.tribal_dimensional_index
    dimension_contribution_to_tdi = tribe.dimension_contribution_to_tdi

    
    
    context = {
        'household': household,
        'total_tribals': total_tribals,
        'tribe': tribe,
        'tribes' : tribes,
        'health_contributions_to_dimension': health_contributions_to_dimension,
        'education_contributions_to_dimension': education_contributions_to_dimension,
        'sol_contributions_to_dimension': sol_contributions_to_dimension,
        'culture_contributions_to_dimension': culture_contributions_to_dimension,
        'governance_contributions_to_dimension': governance_contributions_to_dimension,
        'tribal_dimensional_index': tribal_dimensional_index,
        'dimension_contribution_to_tdi': dimension_contribution_to_tdi,
        'districts' : districts,
        'user' : user,

    }
    return render(request, 'pdfs/tribe_pdf.html', context)


    


