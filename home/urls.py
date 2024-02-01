from django.urls import path
from .views import *


urlpatterns = [
    # path('test/', test_view, name='test'),
    path('tribe-form/', tribe_form_view, name='tribe_form'),
    path('<slug>/pdf/', tribe_pdf_view, name='tribe_pdf'),
    path('<name>/<year>/', tribe_detail_view, name='tribe_detail'), 
]



