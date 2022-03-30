from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import routers

# from .registration import views
# from .views import StudentScheduleSViewSet
from registration import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', include('registration.urls')),
    path('roadmap/', include('roadmap.urls')),
    path('roadmap/api/v1/', include('roadmap.urls')),
    path('', RedirectView.as_view(url='/registration/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('table/', views.table_students, name='table'),
    path('api/', include('registration.urls')),
    path('api/add_name', views.StudentsViewSet.as_view, name='add_name'),
    path('api/add_schedule', views.ScheduleSViewSet.as_view, name='add_schedule'),
    path('api/new_schedule', views.ScheduleAPIView.as_view(), name='new_schedule'),
    path('api/new_schedule/<int:schedule_s_id>', views.OneStudentSchedule.as_view(), name='one_schedule'),
    path('api/new_schedule1/<uuid:id>', views.OneStudentSchedule.as_view(), name='one_schedule'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
