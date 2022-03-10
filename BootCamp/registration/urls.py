from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.RegistrationUserView.as_view(), name='registration'),
    path('check/', views.Check.as_view(), name='check'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
