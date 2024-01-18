from django.urls import path
from .views import *


urlpatterns = [
    # path('test/', test_view, name='test'),
    path('form/', form_view, name='form'),
    path('<slug>/pdf/', tribe_pdf_view, name='tribe_pdf'),
    path('<slug1>/<slug2>/', tribe_detail_view, name='tribe_detail'), 
]



