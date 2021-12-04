from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.schemas import AutoSchema
from .serializers import CropSerializer
from .models import Crop
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


# Create your views here.
class ListCrops(APIView):
     def getcrops(self, request, format=None):
        """
        Return a list of all crops.
        """
        if request.method == 'GET':
         crops = Crop.objects.all()
        crops_serializer = CropSerializer(crops, many=True)
        return JsonResponse(crops_serializer.data, safe=False)