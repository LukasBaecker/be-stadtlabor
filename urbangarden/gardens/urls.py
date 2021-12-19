from django.conf.urls import url
from .views import GardenView, GardenDetailView, GardenDetailViewPost, ResourceView, ResourceDetailView, ResourceDetailViewPost 
from django.urls import path, include

urlpatterns = [
        #Gardens
        path('all', GardenView.as_view()),
        path('<pk>', GardenDetailView.as_view()),
        path('', GardenDetailViewPost.as_view()),
        #Resources
        path('resources/all', ResourceView.as_view()),
        path('resources/<pk>', ResourceDetailView.as_view()),
        path('resources/', ResourceDetailViewPost.as_view()),
]