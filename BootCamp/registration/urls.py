from django.urls import path, include
from rest_framework import routers

# from BootCamp.urls import router
from . import views
from .views import  ScheduleSViewSet, StudentsViewSet

router = routers.DefaultRouter()
# router.register('model', StudentScheduleSViewSet, basename='model')
router.register('add_day', ScheduleSViewSet, basename='add_day')
router.register('get_students', StudentsViewSet, basename='add_name')

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
]
