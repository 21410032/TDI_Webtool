from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [

    path('test/',test_view,name='test'),
    path('form/',form_view,name='form'),
    path('<slug>/',tribe_detail_view,name='tribe_detail'), 
    path('<slug>/pdf/',tribe_pdf_view,name='tribe_pdf'), 

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 