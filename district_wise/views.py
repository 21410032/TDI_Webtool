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
from tablib import Dataset

# Create your views here.
def district_view(request,slug1,slug2):

    user = User.objects.get(phone_number=settings.ADMIN_USER_PHONE_NUMBER)
    districts=District.objects.filter(user = user,year='2022')
    tribes = Tribe.objects.filter(user = user,year='2022').distinct()
    user_phone_number = request.GET.get('user')
    District.objects.filter(W_BMI__isnull=True).delete()
    print(user_phone_number)
    if user_phone_number:
        user = User.objects.get(phone_number=user_phone_number)


    district = District.objects.get(name='Bokaro')

    # Get the score
    print("Multiplier:", district.get_multiplier())

    # Method: get_indicator_st_scores
    print("Indicator ST Scores:", district.get_indicator_st_scores())

    # Method: get_max_min_ind_scores
    max_arr, min_arr = district.get_max_min_ind_scores()
    print("Max Scores:", max_arr)
    print("Min Scores:", min_arr)

    # Method: get_normalized_ind_scores
    print("Normalized Indicator Scores:", district.get_normalized_ind_scores())

    # Method: get_normalized_final_ind_scores
    print("Normalized Final Indicator Scores:", district.get_normalized_final_ind_scores())

    # Method: get_avg_ind_scores
    print("Average Indicator Scores:", district.get_avg_ind_scores())

    # Method: get_dimension_scores
    print("Dimension Scores:", district.get_dimension_scores())

    # Method: get_tdi_score
    geometric_tdi, arithmetic_tdi = district.get_tdi_score()
    print("Geometric TDI:", geometric_tdi)
    print("Arithmetic TDI:", arithmetic_tdi)

    # Method: get_indicator_contri_to_dimension
    indicator_contri_to_dimension = district.get_indicator_contri_to_dimension()
    print("Indicator Contribution to Dimension:", indicator_contri_to_dimension)

    # Method: get_dimension_contribution_tdi
    print("Dimension Contribution to TDI:", district.get_dimension_contribution_tdi())

    # Method: get_score
    print("Overall Score:", district.get_score())

    # Print the data in the terminal

        
    print(user)
    print(districts)


    

    if slug1 is not None and slug2 is not None:
        district = District.objects.get(user = user, slug=slug1, year=slug2)
    print(district)

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
      'districts':districts,
      'district':district,
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
    #   'tribes' : tribes,
      'get_score':get_score,

       

    }

    return render(request, 'district/bokaro.html', context=context)



@login_required
def form_view(request):
    YourModelFormSet = formset_factory(DistrictModelForm, extra=1, can_delete=True, validate_max=True)
    user = User.objects.get(phone_number=settings.ADMIN_USER_PHONE_NUMBER)
   
    districts = District.objects.all().filter(user=user)


    if request.method == 'POST':

        year = request.POST.get('year')
   
        if request.user.is_authenticated:
            user_from_form = request.user  
        else:
            return HttpResponse('Login required')
        
        
        if 'district_excel_file' in request.FILES:
            new_districts = request.FILES['district_excel_file']
            dataset = Dataset()
            imported_districts_dict = dataset.load(new_districts.read(), format='xlsx').dict
            print(imported_districts_dict)


            
            for data in imported_districts_dict:
                district_name = data.get('name').strip()

                if not District.objects.filter(user=user, name=district_name).exists():
                    return HttpResponse(f'District with name "{district_name}" not found. Check your Excel for valid district name.')

                district_data = {
                    'name': data.get('name'),   
                    'year': data.get('year'),    
                    'st_population': data.get('st_population'),    
                    'total_population': data.get('total_population'),    
                    'W_BMI': data.get('W_BMI'),    
                    'C_UW' : data.get('C_UW'),   
                    'AN_W': data.get('AN_W'),    
                    'AN_C' : data.get('AN_C'),   
                    'AHC_ANC'  : data.get('AHC_ANC'),  
                    'AHC_Full_ANC' : data.get('AHC_Full_ANC'),   
                    'AHC_PNC': data.get('AHC_PNC'),    
                    'AHC_HI': data.get('AHC_HI'),    
                    'Enrollment': data.get('Enrollment'),    
                    'Equity': data.get('Equity'),    
                    'E_DropRate': data.get('E_DropRate'),    
                    'S_Sani': data.get('S_Sani'),    
                    'S_CoFu': data.get('S_CoFu'),    
                    'S_DrWa': data.get('S_DrWa'),    
                    'S_Elec': data.get('S_Elec')
                }

                district_form = DistrictModelForm(district_data)
                if district_form.is_valid():
                    district = district_form.save(commit=False)
                    district.user = user_from_form
                    district.save()

                else:
                    print(district_form.errors)
            
            redirect_url = f'/district/bokaro/{year}?user={user_from_form.phone_number}'  # Include user information in the URL
            return redirect(redirect_url)



        else:
            formset = YourModelFormSet(request.POST, prefix='form')
            cleaned_data_list = [] 

        
            for form in formset:
                if form.is_valid():
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


    context = {
    #   'tribes' : tribes,
      'districts' :districts,
    }
    if formset:
        context['formset'] = formset

    return render(request, 'form/district_form.html', context)

