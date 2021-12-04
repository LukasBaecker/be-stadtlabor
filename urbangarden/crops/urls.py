from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from crops.views import *
from django.conf.urls import url 
from .views import ListCrops
 
  
urlpatterns = [ 
    url('', ListCrops.as_view()),
    
]
  
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)