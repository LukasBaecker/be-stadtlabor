from django.conf.urls import url
from .views import GardenView, GardenDetailView, GardenDetailViewPost, ResourceView, ResourceDetailView, ResourceDetailViewPost, GetCoordinatesFromAddress
from django.urls import path, include
from django.urls import path

urlpatterns = [
        #Gardens
        path("coordinates", # the rest will be in views: ?address=QUERY_ADDRESS
          GetCoordinatesFromAddress.as_view(), name="get-coordinates"),
        path('all', GardenView.as_view()),
        path('<pk>', GardenDetailView.as_view()),
        path('', GardenDetailViewPost.as_view()),
       
        #Resources
        path('resources/all', ResourceView.as_view()),
        path('resources/<pk>', ResourceDetailView.as_view()),
        path('resources/', ResourceDetailViewPost.as_view()),
]