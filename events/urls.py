from django.conf.urls import url 
from .views import EventDetailViewPost,EventView,EventDetailView
from django.urls import path, include
from django.views.generic import TemplateView
urlpatterns = [
        path('all', EventView.as_view()),
        path('<pk>', EventDetailView.as_view()),
        path('', EventDetailViewPost.as_view()),
  ]
