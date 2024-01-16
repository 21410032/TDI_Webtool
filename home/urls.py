from django.urls import path
from .views import *


urlpatterns = [

    path('test/',test_view,name='test'),
    path('form/',form_view,name='form'),
    path('<slug>/',tribe_detail_view,name='tribe_detail'), 
    path('<slug>/pdf/',tribe_pdf_view,name='tribe_pdf'), 

]


