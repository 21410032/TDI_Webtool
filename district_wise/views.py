from django.shortcuts import render
from .models import District
from django.shortcuts import render,redirect
from django.contrib import messages
from home.models import Tribe
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.forms import formset_factory
from .forms import DistrictModelForm
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
User = get_user_model()


# Create your views here.
def district_view(request,slug1,slug2):


    user = User.objects.get(phone_number='7667605908')

    if request.method == "POST":
        user = request.user

    districts=District.objects.all().filter(user = user)


    tribes = Tribe.objects.all()
    

    if slug1 is not None and slug2 is not None:
        district = District.objects.get(user = user, name=slug1, year=slug2)


    district_dimensional_index=district.get_dimension_scores()
    tdi=district.get_tdi_score()
    health_ind_contri_to_dim=district.get_indicator_contri_to_dimension()[0]
    education_ind_contri_to_dim=district.get_indicator_contri_to_dimension()[1]
    sol_ind_contri_to_dim=district.get_indicator_contri_to_dimension()[2]
    get_normalized_ind_scores=district.get_normalized_ind_scores()
    normalized_final_ind_scores=district.get_normalized_final_ind_scores()
    health_contri_to_tdi=district.get_dimension_contribution_tdi()[0]
    education_contri_to_tdi=district.get_dimension_contribution_tdi()[1]
    sol_contri_to_tdi=district.get_dimension_contribution_tdi()[2]
    get_score=district.get_score()
    
    context={
      'district':districts,
      'district_dimensional_index':district_dimensional_index,
      'tdi':tdi,
      'health_ind_contri_to_dim':health_ind_contri_to_dim,
      'education_ind_contri_to_dim':education_ind_contri_to_dim,
      'sol_ind_contri_to_dim':sol_ind_contri_to_dim,
      'normalized_final_ind_scores':normalized_final_ind_scores,
      'health_contri_to_tdi':health_contri_to_tdi,
      'education_contri_to_tdi':education_contri_to_tdi,
      'sol_contri_to_tdi':sol_contri_to_tdi,
      'get_normalized_ind_scores':get_normalized_ind_scores,
      'name' : slug1,
    #   'tribes' : tribes,
      'get_score':get_score,

       

    }

    return render(request, 'district/bokaro.html', context=context)

def test2_view(request):
    districts=District.objects.all()
    max_min_arr = districts.first().get_max_min_ind_scores()

    
    context={
        'districts':districts,
        'max_min_arr' : max_min_arr 
    }
    return render(request, 'district/test2.html', context=context)

@login_required
def form_view(request):
    YourModelFormSet = formset_factory(DistrictModelForm, extra=1, can_delete=True, validate_max=True)

    districts = District.objects.all()
    if request.method == 'POST':

        print(f"Raw POST data: {request.POST}")
        formset = YourModelFormSet(request.POST, prefix='form')
        cleaned_data_list = [] 
         # Create a list to store cleaned data for each form
        year = request.POST.get('year')
        print(year)
        for form in formset:
            # Save each form individually
            print(f"Form errors for {form.prefix}: {form.errors}")
            print(f"Field values for {form.prefix}: {form.cleaned_data}")
            if form.is_valid():
                district_instance = form.save(commit=False)
                if request.user.is_authenticated:
                    district_instance.user = request.user
                district_instance.year =year
                    
                district_instance.save()

                # Append cleaned data to the list
                cleaned_data_list.append(form.cleaned_data)
            else:
                print(f"Form errors for {form.prefix}: {form.errors}")
        if cleaned_data_list:
    # Use the last element of the list to construct the redirect URL
            last_data = cleaned_data_list[-1]
            name = last_data['name']
            

    # Construct the redirect URL
            redirect_url = f'/district/{name}/{year}'  # Using f-string for formatting

    # Redirect to the constructed URL
            return redirect(redirect_url)


    else:
        formset = YourModelFormSet(prefix='form')

    return render(request, 'form/district_form.html', {'formset': formset, 'districts': districts})