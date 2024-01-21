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



def tribe_detail_view(request, slug1, slug2):
    print(slug1)
    print(slug2)

    user_phone_number = request.GET.get('user')
    if user_phone_number:
        user = User.objects.get(phone_number=user_phone_number)

    else:    
        user = User.objects.get(phone_number='7667605908')
    print(user)
    tribes = Tribe.objects.filter(user=user).exclude(year='2020').distinct()

    print(tribes)
    if slug1 and slug2 is not None:
         tribe = Tribe.objects.filter(user=user,name = slug1,year=slug2)
        
    print(tribe)
    total_tribals = tribe.get_total_tribals()
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

    # return render(request, 'base.html')



# def test_view(request):
    
#     tribe = Tribe.objects.get(id = 2)
#     total_tribals = tribe.get_total_tribals
#     household = Household.objects.all()
    
    
    
#     context = {
#         'household' : household,
#         'total_tribals' : total_tribals,
#         'tribe' : tribe,
        

#     }
#     return render(request, 'pvtg/test.html', context)

def form_view(request):
    YourModelFormSet = formset_factory(HouseholdForm, extra=1, can_delete=True, validate_max=True)
    user = User.objects.get(phone_number='7667605908')
    tribes = Tribe.objects.filter(user=user, year='2022').distinct()
    alltribes = Tribe.objects.all()

    if request.method == 'POST':
        formset = YourModelFormSet(request.POST, prefix='form')
        cleaned_data_list = []

        # Set the initial year for each form
        year = request.POST.get('year')
        tribeID = request.POST.get('tribeID')

        user_from_form = request.user if request.user.is_authenticated else user

        tribeID = request.POST.get('tribeID')
        print(f'Tribe ID: {tribeID}')

        for form in formset:
            if form.is_valid():
  
            
                
                tribe, created = Tribe.objects.get_or_create(user = request.user, year = year, slug=tribeID)

                household = form.save(commit=False)
                household.tribe = tribe
                household.save()
                cleaned_data_list.append(form.cleaned_data)

                # Print form data
                print(f'Form Data: {form.cleaned_data}')

        if cleaned_data_list:
            redirect_url = f'/tribe/{tribeID}/{year}?user={user_from_form.phone_number}'
            return redirect(redirect_url)
       

    else:
        formset = YourModelFormSet(prefix='form')

    return render(request, 'form/form.html', {'formset': formset, 'tribes': tribes, 'alltribes': alltribes})

    

    
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


    


