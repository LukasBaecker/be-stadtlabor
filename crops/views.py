import coreapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.schemas import AutoSchema
from .serializers import CropSerializer
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from gardens.models import Garden
from crops.models import Crop
import jwt
from rest_framework import status
from rest_framework.parsers import JSONParser


class CropViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post', 'put']:
            extra_fields = [
                coreapi.Field(
                    name = 'name',
                    required = True,
                    description= 'Crop Name: Name of the crop',
                    type='string'), 
                coreapi.Field(
                    name = 'description',
                    required = True,
                    description= 'Chracteristics, details, aim (etc): In the event we will discover ...',
                    type='string'),
                coreapi.Field(
                    name = 'characteristics',
                    required = True,
                    description= 'The charcteristics of the crop',
                    type='string'),
                coreapi.Field(
                    name = 'image',
                    required = True,
                    description= 'Picture of the crop',
                    type='string'),
                coreapi.Field(
                    name = 'gardens',
                    required = True,
                    description= 'Garden id: 1 or 2 or 3 ...',
                    type='integer'),   
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields

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
           
class CropDetailView(APIView):
   schema=CropViewSchema()   
   def put(self,request,pk):
     token = request.COOKIES.get('jwt')
     if not token:
            raise AuthenticationFailed('Unauthenticated!')
     try:
            crop = Crop.objects.get(pk=pk) 
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
     except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

     crop_data = JSONParser().parse(request) 
     crop_serializer = CropSerializer(crop, data=crop_data) 
     if crop_serializer.is_valid(): 
            crop_serializer.save() 
            return JsonResponse(crop_serializer.data) 
     return JsonResponse(crop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                   