from django.conf.urls import url
from gardens.views import GardenView, GardenDetailView, GardenDetailViewPost, ResourceView, ResourceDetailView, ResourceDetailViewPost 
from django.urls import path, include
from rest_framework import routers


router = routers.DefaultRouter()
router.register('', GardenView)


urlpatterns = [
        #Gardens
        #path('all', GardenView),
        path('<pk>', GardenDetailView.as_view()),
        path('', GardenDetailViewPost.as_view()),
        path('all/', include(router.urls)),
        #Resources
        path('resources/all', ResourceView.as_view()),
        path('resources/<pk>', ResourceDetailView.as_view()),
        path('resources/', ResourceDetailViewPost.as_view()),
]
