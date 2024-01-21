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


    user_phone_number = request.GET.get('user')
    if user_phone_number:
        user = User.objects.get(phone_number=user_phone_number)


    else:    
        user = User.objects.get(phone_number='7219142469')

    District.objects.filter(W_BMI__isnull=True).delete()
    districts=District.objects.filter(user = user)



    tribes = Tribe.objects.all()
    

    if slug1 is not None and slug2 is not None:
        district = District.objects.get(user = user, slug=slug1, year=slug2)


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
    user = User.objects.get(phone_number='7667605908')
   
    districts = District.objects.all().filter(user=user)


    if request.method == 'POST':
        formset = YourModelFormSet(request.POST, prefix='form')
        print(request.POST)
        cleaned_data_list = [] 

        year = request.POST.get('year')
        user_from_form = request.user if request.user.is_authenticated else user  # Use the user from the form if authenticated, otherwise use the default user

        # ...

        for form in formset:
            if form.is_valid():
                print(form.cleaned_data)
                # Check if the form's cleaned data includes the DELETE field
                if form.cleaned_data.get('DELETE', False):
                    district_instance = form.instance
                    district_instance.delete()
                else:
                    district_instance = form.save(commit=False)
                    district_instance.user = user_from_form
                    district_instance.year = year
                    district_instance.save()
                    cleaned_data_list.append(form.cleaned_data)

# ...



        if cleaned_data_list:
            redirect_url = f'/district/bokaro/{year}?user={user_from_form.phone_number}'  # Include user information in the URL
            return redirect(redirect_url)


    else:
        formset = YourModelFormSet(prefix='form')

    return render(request, 'form/district_form.html', {'formset': formset, 'districts': districts})

