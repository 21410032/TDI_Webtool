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
import pandas as pd
import numpy as np
from tablib import Dataset
from .resources import *


# Create your views here.
from .forms import HouseholdForm
from django.forms import formset_factory



def tribe_detail_view(request, name, year):
    
    user = User.objects.get(phone_number=settings.ADMIN_USER_PHONE_NUMBER)
    Household.objects.filter(size__isnull=True).delete()
    tribes = Tribe.objects.filter(user = user, year='2022')
    districts=District.objects.filter(user = user, year='2022')
    print(user)
    print(name)
    print(year)
    tribe_of_slug = Tribe.objects.get(user=user, year = '2022', name = name)
   
    user_phone_number = request.GET.get('user')

    if user_phone_number:
        user = User.objects.get(phone_number=user_phone_number)

    else:    
        user = User.objects.get(phone_number=settings.ADMIN_USER_PHONE_NUMBER)

    

    if name and year is not None:
        try:
            
            tribe = Tribe.objects.get(user=user, year=year, name = name)
            
        except Exception as e:
            return e 

    # tribe_of_slug = Tribe.objects.get(slug = slug1)
    total_tribals = tribe.get_total_tribals
    household = Household.objects.all()
    
    contributions_to_dimension = tribe.indicator_contributions_to_dimension

    health_contributions_to_dimension = contributions_to_dimension[0] if contributions_to_dimension and len(contributions_to_dimension) > 0 else None
    education_contributions_to_dimension = contributions_to_dimension[1] if contributions_to_dimension and len(contributions_to_dimension) > 1 else None
    sol_contributions_to_dimension = contributions_to_dimension[2] if contributions_to_dimension and len(contributions_to_dimension) > 2 else None
    culture_contributions_to_dimension = contributions_to_dimension[3] if contributions_to_dimension and len(contributions_to_dimension) > 3 else None
    governance_contributions_to_dimension = contributions_to_dimension[4] if contributions_to_dimension and len(contributions_to_dimension) > 4 else None

    tribal_dimensional_index = tribe.tribal_dimensional_index
    dimension_contribution_to_tdi = tribe.dimension_contribution_to_tdi
    

    
    context = {
        'tribes' : tribes,
        'districts' :districts,
        'household': household,
        'total_tribals': total_tribals,
        'tribe_of_slug':tribe_of_slug,
        'tribe': tribe,
        'health_contributions_to_dimension': health_contributions_to_dimension,
        'education_contributions_to_dimension': education_contributions_to_dimension,
        'sol_contributions_to_dimension': sol_contributions_to_dimension,
        'culture_contributions_to_dimension': culture_contributions_to_dimension,
        'governance_contributions_to_dimension': governance_contributions_to_dimension,
        'tribal_dimensional_index': tribal_dimensional_index,
        'dimension_contribution_to_tdi': dimension_contribution_to_tdi,
    }
        


    return render(request, 'pvtg/asur.html', context=context)

import pandas as pd
from .test2 import perform_calculations

@login_required(login_url='/accounts/login/')
def tribe_form_view(request):
    user = User.objects.get(phone_number=settings.ADMIN_USER_PHONE_NUMBER)
    tribes = Tribe.objects.filter(user=user, year = '2022').distinct()
    alltribes_defined=Tribe.objects.filter(user = user)
    YourModelFormSet = formset_factory(HouseholdForm, extra=1, can_delete=True, validate_max=True)
    if request.method == 'POST':


        year = request.POST.get('year')
       
        if request.user.is_authenticated:
            user_from_form = request.user  #user instance
        else:
            return HttpResponse('Login first')
        
          #tribe instance
        
        if 'households_excel_file' in request.FILES:
            uploaded_file  = request.FILES['households_excel_file']
            
            #create dataframe of base_data
            base_data_df = pd.read_excel(uploaded_file)

            perform_calculations(base_data_df, user_from_form, year)
            
            
            redirect_url = f'/tribe/असुर/{request.POST["year"]}?user={user_from_form.phone_number}'
            return redirect(redirect_url)
        else:
            tribe_slug = request.POST.get('tribe_slug')
            cleaned_data_list = []
            formset = YourModelFormSet(request.POST, prefix='form')
        
            if formset.is_valid():
                for form in formset:
                    
                    tribe, created = Tribe.objects.get_or_create(user=request.user, year=year, name=tribe_slug)
                    household = form.save(commit=False)
                    household.tribeID = tribe
                    household.save()
                    cleaned_data_list.append(household)
            else:
                # Print form errors to understand why validation failed
                ##print(formset.errors)
    
                    

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



def test_view(request):
    user = User.objects.get(phone_number=settings.ADMIN_USER_PHONE_NUMBER)

    tribe = Tribe.objects.get(id = 1155)

    total_tribals = tribe.get_total_tribals
    household = Household.objects.filter(tribeID = tribe)
    
    
    
    context = {
        'household' : household,
        'total_tribals' : total_tribals,
        'tribe' : tribe,
        

    }
    return render(request, 'pvtg/test.html', context)