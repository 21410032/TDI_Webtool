from django.shortcuts import render
from home.models import Tribe, User_Hitcounts
from district_wise.models import District

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.
from django.conf import settings


def home_view(request):
    user = User.objects.get(phone_number='7667605908')
    tribes = Tribe.objects.all()
    districts=District.objects.filter(user = user)
    user = request.user

    tribe_wise_tdi = []
    for tribe in tribes:
        tribe_wise_tdi.append(tribe.tribal_index)
    


    districts_name = []
    for district in districts:
        districts_name.append(district.name)


    district_wise_tdi = []
    for district in districts:
        district_wise_tdi.append(district.get_tdi_score()[0])

    context = {
        'tribes' : tribes,
        'district' :districts,
        'tribe_wise_tdi' : tribe_wise_tdi,
        'districts_name' : districts_name,
        'district_wise_tdi' : district_wise_tdi,
        'user' : user,
    }


# Visitors Count
# Increment the total site views
    User_Hitcounts.increment_site_views()

    # Retrieve the total site views
    total_site_views = User_Hitcounts.get_site_views()

    # Pass the total_site_views to the template context
    context['total_site_views'] = total_site_views

    return render(request,'home/homepage.html',context=context)



def wallpaper_view(request):
    return render(request,'gallery.html')


def base_view(request):
    tribes = Tribe.objects.all()
    districts = District.objects.all()

    tribe_wise_tdi = []
    for tribe in tribes:
        tribe_wise_tdi.append(tribe.tribal_index)
    


    districts_name = []
    for district in districts:
        districts_name.append(district.name)


    district_wise_tdi = []
    for district in districts:
        district_wise_tdi.append(district.get_tdi_score()[0])

    context = {
        'tribes' : tribes,
        'districts' :districts,
        'tribe_wise_tdi' : tribe_wise_tdi,
        'districts_name' : districts_name,
        'district_wise_tdi' : district_wise_tdi,
    }
    return render(request,'base.html',context=context)