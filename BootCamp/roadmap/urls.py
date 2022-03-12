from django.urls import path

from . import views
from .views import ViewEvent, DetailEvent, ListAcceptEvents, DetailAcceptEvents, indexUsers, index

urlpatterns = [
    path('', index.as_view()),
    path('<int:pk>', indexUsers.as_view()),
    path('myevents', ViewEvent.as_view()),
    path('myevents/<int:pk>', DetailEvent.as_view()),
    path('acceptevents', ListAcceptEvents.as_view()),
    path('acceptevents/<int:pk>', DetailAcceptEvents.as_view()),
]