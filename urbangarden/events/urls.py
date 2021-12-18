from django.conf.urls import url 
from .views import EventView
from django.urls import path, include
urlpatterns = [
    path('', EventView.as_view()),
    path('pk', EventView.as_view()),

]
 
