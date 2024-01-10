from django.shortcuts import render
from .models import District
from django.shortcuts import render,redirect
from django.contrib import messages
from home.models import Tribe
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseBadRequest


# Create your views here.
def district_view(request,slug1,slug2):
    districts=District.objects.all()
    tribes = Tribe.objects.all()

    if slug1 is not None and slug2 is not None:
       district = District.objects.get(slug=slug1, year=slug2)


      
    # if slug1 is not None:
    #     try:
    #         district = District.objects.filter(name=slug1)
    #     except District.DoesNotExist:
    #         raise Http404
    #     if slug2 is not None:
    #         try:
    #            district = District.objects.filter(year=slug2)
    #         except District.DoesNotExist:
    #            raise Http404


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
      'tribes' : tribes,
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

def form_view(request):
    districts = District.objects.all()
    context = {
        'districts':districts,
    }
    if request.method == "POST":
        district_name= request.POST.get('district_name')
        print(district_name)
        st_population = request.POST.get('st_population')
        tot_population = request.POST.get('tot_population')

        # try:
        #     district = District.objects.get(id=district_id)
        # except District.DoesNotExist:
        #     # Handle the case where the selected tribe doesn't exist
        #     return HttpResponse('Selected tribe does not exist')
        
        
        
        district_object = District.objects.create(
            name= district_name,
            year=request.POST.get('Year'),
            st_population = st_population,
            total_population=tot_population,
            W_BMI = request.POST.get('Women_whose_BMI_is_below_normal'),
            C_UW = request.POST.get('Children_under_5_years_who_are_underweight'),
            AN_W = request.POST.get('Women_age_15_to_49_years_who_are_anaemic'),
            AN_C = request.POST.get('Children_age_6_to_59_months_who_are_anaemic'),
            AHC_ANC = request.POST.get('Antenatal_care_in_first_trimester'),
            AHC_Full_ANC = request.POST.get('Full_antenatal_care'),
            AHC_PNC = request.POST.get('Post_natal_care'),
            AHC_HI = request.POST.get('Health_insurance'),
            Enrollment = request.POST.get('Enrolment'),
            Equity = request.POST.get('Equity_Outcome'),
            E_DropRate = request.POST.get('Drop_out_rate'),
            S_Sani = request.POST.get('IC_score'),
            S_CoFu = request.POST.get('Source_of_cooking_fuel'),
            S_DrWa = request.POST.get('Source_of_drinking_water'),
            S_Elec = request.POST.get('Electricity'),
            
        )
        district_object.save()
        name=district_name,
        year=request.POST.get('Year'),
        if not year:
            messages.error(request, 'Please provide a value for the Year field.')
            return HttpResponseBadRequest("Year field is required.")

        try:
            year = int(year[0])  # Convert 'year' to integer
        except ValueError:
            # Handle the case where 'year' is not a valid integer
            messages.error(request, 'Invalid year value. Please provide a valid integer for the year.')
            return HttpResponseBadRequest("Invalid year value.")
        messages.success(request, 'Household added successfully!!!')
        print(name)
        print(year)
        return redirect('district_view', slug1=name[0], slug2=year)


    return render(request, 'form/district_form.html',context=context)