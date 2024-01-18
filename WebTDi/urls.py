from django.contrib import admin
from django.urls import path,include
from .views import home_view
from django.conf import settings
from django.conf.urls.static import static
from .views import wallpaper_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('tribe/', include('home.urls')),
    path('district/', include('district_wise.urls')),
    path('accounts/', include('accounts.urls')),
    path('gallery/',wallpaper_view),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 