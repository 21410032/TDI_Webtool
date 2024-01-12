from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import Http404
from .models import Household, Tribe
from district_wise.models import District
from django.http import HttpResponse
# Create your views here.
from .forms import TribeModelForm
from django.forms import formset_factory

def tribe_detail_view(request, slug):
    tribes = Tribe.objects.all()
    if slug is not None:
        try:
            tribe = Tribe.objects.get(slug=slug)
        except Tribe.DoesNotExist:
            raise Http404
        except tribe.MultipleObjectsReturned:
            tribe=tribe.objects.filter(slug=slug).first()
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
    
    YourModelFormSet = formset_factory(TribeModelForm, extra=1, can_delete=True, validate_max=True)

    if request.method == 'POST':
        print(f"Raw POST data: {request.POST}")
        formset = YourModelFormSet(request.POST, prefix='form')
        
        for form in formset:
                # Save each form indsividually
            print(f"Form errors for {form.prefix}: {form.errors}")
                
            print(f"Field values for {form.prefix}: {form.cleaned_data}")
            if form.is_valid():
             form.save()

            # Redirect after successful form submission to avoid resubmission on page refresh
        return redirect('/')  # Replace 'success_page' with the actual URL or name of your success page
    else:
        formset = YourModelFormSet(prefix='form')

    return render(request, 'form/form.html', {'formset': formset})
    tribes = Tribe.objects.all()
    context = {
        'tribes':tribes,
    }
    if request.method == "POST":
        tribe_id = request.POST.get('tribe_id')
        size = request.POST.get('HH_size')

        try:
            tribe = Tribe.objects.get(id=tribe_id)
        except Tribe.DoesNotExist:
            # Handle the case where the selected tribe doesn't exist
            return HttpResponse('Selected tribe does not exist')
        
        
        
        HH_object = Household.objects.create(
            tribeID = tribe,
            size = size,
            CD_score = request.POST.get('CD_score'),
            IM_score = request.POST.get('IM_score'),
            MC_score = request.POST.get('MC_score'),
            CM_score = request.POST.get('CM_score'),
            FS_score = request.POST.get('FS_score'),
            LE_score = request.POST.get('LE_score'),
            DRO_score = request.POST.get('DRO_score'),
            IC_score = request.POST.get('IC_score'),
            OW_score = request.POST.get('OW_score'),
            SANI_score = request.POST.get('SANI_score'),
            FUEL_score = request.POST.get('FUEL_score'),
            DRWA_score = request.POST.get('DRWA_score'),
            ELECTR_score = request.POST.get('ELECTR_score'),
            ASS_score = request.POST.get('ASS_score'),
            LAN_score = request.POST.get('LAN_score'),
            ARTS_score = request.POST.get('ARTS_score'),
            EV_score = request.POST.get('EV_score'),
            MEET_score = request.POST.get('MEET_score'),
        )
        HH_object.save()
        messages.success(request, 'Household added successfully!!!')
        return redirect('form')


    return render(request, 'form/form.html',context=context)