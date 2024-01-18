from django.contrib import admin
from django.urls import path,include
from .views import home_view
from .views import wallpaper_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('tribe/', include('home.urls')),
    path('district/', include('district_wise.urls')),
    path('accounts/', include('accounts.urls')),
    path('gallery/',wallpaper_view),
]
