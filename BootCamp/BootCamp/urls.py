from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', include('registration.urls')),
    path('roadmap/', include('roadmap.urls')),
    path('roadmap/api/v1/', include('roadmap.urls')),
    path('', RedirectView.as_view(url='/registration/', permanent=True)),
]
