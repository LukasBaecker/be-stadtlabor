from math import nan
from django.http import response
from django.shortcuts import render

from django.template import RequestContext
from django.http.response import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
import requests
from .models import Garden, Resource
from .serializers import GardenSerializer, ResourceSerializer
from django.urls import reverse
from rest_framework.decorators import api_view
import coreapi


from django.http.response import JsonResponse
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework.parsers import JSONParser
from rest_framework import status, viewsets

from .models import Garden, Resource
from .serializers import GardenSerializer, ResourceSerializer, NearestGardenSerializer


from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
import geocoding
from django.shortcuts import render
from django.http import  HttpResponse
import urllib,json
from geopy.geocoders import Nominatim
from rest_framework.generics import ListAPIView
from rest_framework_gis.filterset import GeoFilterSet        
from rest_framework.decorators import action

import coreapi
import jwt 
#CoreAPI schema -> Brian Pondi 

class GardenViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post', 'put']:
            extra_fields = [
                coreapi.Field(
                    name = 'longitude',
                    required = True,
                    description= 'Decimal degrees (float): 7.626143',
                    type='number'),
                coreapi.Field(
                    name = 'latitude',
                    required = True,
                    description= 'Decimal degrees (float): 51.960745',
                    type='number'),
                coreapi.Field(
                    name = 'name',
                    required = True,
                    description= 'Garden name: Der Paradeiser',
                    type='string'),
                coreapi.Field(
                    name = 'description',
                    required = True,
                    description= 'Chracteristics, details, aim (etc): The garden consists of 16 raised beds ...',
                    type='string'),
                coreapi.Field(
                    name = 'email',
                    required = True,
                    description= 'Official email: Garden@email.com',
                    type='string'),
                coreapi.Field(
                    name = 'phone',
                    required = True,
                    description= 'Phone number with country code: +49 1 575123456',
                    type='string'),
                coreapi.Field(
                    name = 'crops',
                    required = True,
                    description= 'Array of crops id [1,4,6]: 1 = Beetroot, 2 = Marsh bedstraw ...',
                    type='string'),
                coreapi.Field(
                    name = 'address',
                    required = True,
                    description= 'Name and number: Gardenstrasse 1',
                    type='string'),
                coreapi.Field(
                    name = 'geom_point',
                    required = True,
                    description= '''Location of garden (supports WKT or geojson geometries):
                    {
                        "type": "Point",
                        "coordinates": 
                            [ -0.034294116776437,
                            0.018081666485151  ]
                    }''',
                    type='string'),
                coreapi.Field(
                    name = 'geom_polygon',
                    required = True,
                    description= '''Limit of garden (supports WKT or geojson geometries):
                    {
                        "type": "Polygon",
                        "coordinates": 
                        [ [ [ -0.002861015964299, 0.035667405488396 ],
                          [  0.062141418457031, 0.039939849196801 ],
                          [  0.029487619176507, 0.054588288657813 ],
                          [ -0.002861015964299, 0.035667405488396 ] ] ] 
                    }''',
                    type='string'),
                coreapi.Field(
                    name = 'primary_purpose',
                    required = True,
                    description= '"Garden" or "Resources"',
                    type='string'),           
                coreapi.Field(
                    name = 'members',
                    required = True,
                    description= 'User members',
                    type='string'),                
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields

class ResourceViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post', 'put']:
            extra_fields = [
                coreapi.Field(
                    name = 'resource_status',
                    required = True,
                    description= '"Available for borrowing" or "Borrowed" or "Available for donation"',
                    type='string'),
                coreapi.Field(
                    name = 'resource_name',
                    required = True,
                    description= 'Resource name: Hammer',
                    type='string'),
                coreapi.Field(
                    name = 'description',
                    required = True,
                    description= 'Chracteristics, details, aim (etc): The tool is made of ...',
                    type='string'),
                coreapi.Field(
                    name = 'category',
                    required = True,
                    description= 
                    ''' Category:
                    1 = Tools, 2 = Seeds, 3 = Fertilizers,
                    4 = Compost, 5 = Construction_materials,
                    6 = Gardens, 7 = Others''',
                    type='integer'),
                coreapi.Field(
                    name = 'date_created',
                    required = True,
                    description= '2021-12-16 T12:00:00Z',
                    type='string'),
                coreapi.Field(
                    name = 'return_date',
                    required = True,
                    description= '2021-12-16 T12:00:00Z',
                    type='string'),
                coreapi.Field(
                    name = 'garden',
                    required = True,
                    description= 'Garden id: 1 or 2 or 3 ...',
                    type='integer'),                  
                coreapi.Field(
                    name = 'lender_id',
                    required = True,
                    description= 'User id: 1 or 2 or 3 ...',
                    type='integer'), 
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


#Javier Martín - 04/12/2021

# Create your views here.

# GARDENS
# 1 of 2: request for all ['GET']
class GardenView(viewsets.ReadOnlyModelViewSet):
    schema =GardenViewSchema()
    serializer_class = NearestGardenSerializer
    queryset = Garden.objects.all()

    #Brian
    @action(detail=False, methods=['get'])
    def get_nearest_gardens(self, request):
        x_coords = request.GET.get('x', None)
        y_coords = request.GET.get('y', None)
        if x_coords and y_coords:
            user_location = Point(float(x_coords), float(y_coords),srid=4326)
            nearest_gardens = Garden.objects.annotate(distance=Distance('geom_point',user_location)).order_by('distance')#[:3]
            serializer = self.get_serializer_class()
            serialized = serializer(nearest_gardens, many = True)
            print(nearest_gardens)
            return JsonResponse(serialized.data, status=status.HTTP_200_OK)
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

# 2 of 2: request by garden ID ['GET', 'PUT', 'DELETE']

class GardenDetailView(APIView):
    schema =GardenViewSchema()

    def get(self,request,pk):
        garden = Garden.objects.get(pk=pk)
        garden_serializer = GardenSerializer(garden) 
        return JsonResponse(garden_serializer.data) 
 
    def put(self,request,pk): 
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            garden = Garden.objects.get(pk=pk)
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        garden_data = JSONParser().parse(request) 
        garden_serializer = GardenSerializer(garden, data=garden_data) 
        if garden_serializer.is_valid(): 
            garden_serializer.save() 
            return JsonResponse(garden_serializer.data) 
        return JsonResponse(garden_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    def delete(self,request,pk):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            garden = Garden.objects.get(pk=pk)
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        garden.delete() 
        return JsonResponse({'message': 'Garden was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

class GardenDetailViewPost(APIView):
    schema =GardenViewSchema()

    def post(self,request): 
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        garden_data = JSONParser().parse(request) 
        location=[]
        if garden_data["latitude"]==nan and garden_data["longitude"]==nan:
            garden_data["latitude"]=geocoding.geocoder[0]
            garden_data["longitude"]=geocoding.geocoder[1]
        garden_data["latitude"]=location[0]
        garden_data["longitude"]=location[1]
        print(location)    
        garden_serializer = GardenSerializer(data=garden_data) 
        if garden_serializer.is_valid(): 
            garden_serializer.save() 
            return JsonResponse(garden_serializer.data) 
        return JsonResponse(garden_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
  


# RESOURCES
# 1 of 2: request for all ['GET']
class ResourceView(APIView):
    schema =ResourceViewSchema()
    def get(self,request):

        if request.method == 'GET':
            resources = Resource.objects.all()
            resource_serializer = ResourceSerializer(resources, many=True)
            return JsonResponse(resource_serializer.data, safe=False)
        
# 2 of 2: request by resource ID ['GET', 'PUT', 'DELETE']

class ResourceDetailView(APIView):
    schema =ResourceViewSchema()
    
    def get(self,request,pk):
        resource = Resource.objects.get(pk=pk) 
        resource_serializer = ResourceSerializer(resource) 
        return JsonResponse(resource_serializer.data) 
    
    def put(self,request,pk):
        token = request.COOKIES.get('jwt')
        if not token:
                raise AuthenticationFailed('Unauthenticated!')
        try:
            resource = Resource.objects.get(pk=pk)  
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        resource_data = JSONParser().parse(request) 
        resource_serializer = ResourceSerializer(resource, data=resource_data) 
        if resource_serializer.is_valid(): 
            resource_serializer.save() 
            return JsonResponse(resource_serializer.data) 
        return JsonResponse(resource_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self,request,pk):
        token = request.COOKIES.get('jwt')
        if not token:
                raise AuthenticationFailed('Unauthenticated!')
        try:
                resource = Resource.objects.get(pk=pk) 
                payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!')

        resource.delete() 
        return JsonResponse({'message': 'Resource was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

class ResourceDetailViewPost(APIView):
    schema =ResourceViewSchema()

    def post(self,request): 
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        resource_data = JSONParser().parse(request) 
        resource_serializer = ResourceSerializer(data=resource_data) 
        if resource_serializer.is_valid(): 
            resource_serializer.save() 
            return JsonResponse(resource_serializer.data) 
        return JsonResponse(resource_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

