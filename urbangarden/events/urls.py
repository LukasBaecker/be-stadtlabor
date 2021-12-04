from django.conf.urls import url 
from events import views 
 
urlpatterns = [ 
    url('', views.event_list),
    url('pk', views.event_detail),
    
]