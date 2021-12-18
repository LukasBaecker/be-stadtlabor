from django.conf.urls import url 
from .views import EventView,EventDetailView
from django.urls import path, include
from django.views.generic import TemplateView
urlpatterns = [
   path('', EventView.as_view()),
   path('<pk>/', EventDetailView.as_view()),   
  ]
