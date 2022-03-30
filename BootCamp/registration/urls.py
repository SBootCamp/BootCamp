from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.RegistrationUserView.as_view(), name='registration'),
    path('check/', views.Check.as_view(), name='check'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
