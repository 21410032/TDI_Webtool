from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import Http404
from .models import Household, Tribe,Tribe_Image
from district_wise.models import District
from django.http import HttpResponse
from django.contrib.auth import get_user_model
User = get_user_model()
from django.conf import settings
from django.contrib.auth.decorators import login_required

from tablib import Dataset
from .resources import *


# Create your views here.
from .forms import HouseholdForm
from django.forms import formset_factory



def tribe_detail_view(request, slug1, slug2):
    user = User.objects.get(phone_number=settings.ADMIN_USER_PHONE_NUMBER)
    print(user)
    tribe_of_slug = Tribe.objects.get(user=user, year = '2022', slug = slug1)
    print(tribe_of_slug)
    user_phone_number = request.GET.get('user')
    print(user_phone_number)
    if user_phone_number:
        user = User.objects.get(phone_number=user_phone_number)

    else:    
        user = User.objects.get(phone_number=settings.ADMIN_USER_PHONE_NUMBER)
    print(user)
    tribes = Tribe.objects.filter(user=user, year = '2022').distinct()
    print(tribes)
    if slug1 and slug2 is not None:
        try:
            
            tribe = Tribe.objects.get(user=user, year=slug2, slug = slug1)
            
        except Exception as e:
            return e 
    print(tribe)
    # tribe_of_slug = Tribe.objects.get(slug = slug1)
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

    # print(tribe_of_slug.tribe_image.first.map_image.url)
    
    context = {
        'household': household,
        'total_tribals': total_tribals,
        'tribe_of_slug':tribe_of_slug,
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

@login_required(login_url='/accounts/login/')
def tribe_form_view(request):
    user = User.objects.get(phone_number=settings.ADMIN_USER_PHONE_NUMBER)
    tribes = Tribe.objects.filter(user=user, year = '2022').distinct()
    alltribes_defined=Tribe.objects.filter(user = user)
    YourModelFormSet = formset_factory(HouseholdForm, extra=1, can_delete=True, validate_max=True)
    if request.method == 'POST':


        year = request.POST.get('year')
        tribe_slug = request.POST.get('tribe_slug')
        print(tribe_slug)
        if request.user.is_authenticated:
            user_from_form = request.user  #user instance
        else:
            return HttpResponse('Login first')
        
          #tribe instance
        
        if 'households_excel_file' in request.FILES:
            new_households = request.FILES['households_excel_file']
            household_resource = HouseholdResource()
            dataset = Dataset()
            imported_households = dataset.load(new_households.read(), format = 'xlsx')
            imported_households_dict = dataset.dict

            
            for data in imported_households_dict:
                slug = data.get('tribeID')

                if not Tribe.objects.filter(user=user, slug=slug).exists():
                    return HttpResponse(f'Tribe with slug "{slug}" not found. Check your Excel for valid tribe name.')
                
                tribe, created = Tribe.objects.get_or_create(user = request.user,year = year, name = slug, slug=slug)

                household_data = {
                    'tribe_slug':slug,
                    'size': data.get('size'),
                    'CD_score':bool(data.get('CD_score')),
                    'IM_score':bool(data.get('IM_score')),
                    'MC_score':bool(data.get('MC_score')),
                    'CM_score':bool(data.get('CM_score')),
                    'FS_score':bool(data.get('FS_score')),
                    'LE_score':bool(data.get('LE_score')),
                    'DRO_score':bool(data.get('DRO_score')),
                    'IC_score':bool(data.get('IC_score')),
                    'OW_score':bool(data.get('OW_score')),
                    'SANI_score':bool(data.get('SANI_score')),
                    'FUEL_score':bool(data.get('FUEL_score')),
                    'DRWA_score':bool(data.get('DRWA_score')),
                    'ELECTR_score':bool(data.get('ELECTR_score')),
                    'ASS_score':bool(data.get('ASS_score')),
                    'LAN_score':bool(data.get('LAN_score')),
                    'ARTS_score':bool(data.get('ARTS_score')),
                    'EV_score':bool(data.get('EV_score')),
                    'MEET_score':bool(data.get('MEET_score'))
                }
                household_form = HouseholdForm(household_data)
                if household_form.is_valid():
                    household = household_form.save(commit=False)
                    household.tribeID = tribe
                    household.save()

                else:
                    print(household_form.errors)
            
            if tribe_slug is not None:
                redirect_url = f'/tribe/{tribe_slug}/{request.POST["year"]}?user={user_from_form.phone_number}'
            else:
                tribe_slug = 'asur'
                redirect_url = f'/tribe/{tribe_slug}/{request.POST["year"]}?user={user_from_form.phone_number}'
            return redirect(redirect_url)


                

            
        else:
            cleaned_data_list = []
            formset = YourModelFormSet(request.POST, prefix='form')
        
            if formset.is_valid():
                for form in formset:
                    
                    tribe, created = Tribe.objects.get_or_create(user=request.user, year=year, name=tribe_slug, slug=tribe_slug)
                    household = form.save(commit=False)
                    household.tribeID = tribe
                    household.save()
                    cleaned_data_list.append(household)
            
            
            else:
                # Print form errors to understand why validation failed
                print(formset.errors)
    
                    

            if cleaned_data_list:
                redirect_url = f'/tribe/{tribe_slug}/{request.POST["year"]}?user={user_from_form.phone_number}'
                return redirect(redirect_url)


    else:
        formset = YourModelFormSet(prefix='form')

    context = {
        'tribes': tribes,
        'alltribes':alltribes_defined,
    }

    if formset:
        context['formset'] = formset
    return render(request, 'form/tribe_form.html',context)

    
    

    
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
