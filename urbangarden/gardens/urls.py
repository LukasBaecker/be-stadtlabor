from django.conf.urls import url
from gardens import views

urlpatterns = [
        #Gardens
        url('gardens/all', views.garden_all),
        url('gardens/ID/(?P<pk>[0-9]+)', views.garden_ID),
        #Resources
        url('resources/all', views.resource_all),
        url('resources/ID/(?P<pk>[0-9]+)', views.resource_ID)
]