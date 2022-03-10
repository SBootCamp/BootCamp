from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>', views.indexUsers, name='indexUser'),
    path('api/v1/test/myevents', ViewEvent.as_view()),
    path('api/v1/test/myevents/<int:pk>', DetailEvent.as_view()),
    path('api/v1/test/acceptevents', ListAcceptEvents.as_view()),
    path('api/v1/test/acceptevents/<int:pk>', DetailAcceptEvents.as_view()),
]