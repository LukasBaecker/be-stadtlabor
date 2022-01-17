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
from rest_framework.decorators import api_view
from gardens.models import Garden

# Create your views here.
@api_view(['GET'])
def getcrops(request):
        """
        Return a list of all crops.
        """
        if request.method == 'GET':
           crops = Crop.objects.all()
           crop_serializer = CropSerializer(crops, many=True)
           return JsonResponse(crop_serializer.data, safe=False)

  
      
              

