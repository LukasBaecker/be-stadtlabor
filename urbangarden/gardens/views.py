from django.shortcuts import render

from django.http.response import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import Garden, Resource
from .serializers import GardenSerializer, ResourceSerializer

from rest_framework.decorators import api_view
import coreapi
from rest_framework.schemas import AutoSchema
import jwt 
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed

#CoreAPI schema -> Brian Pondi 

class GardenViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post', 'put']:
            extra_fields = [
                coreapi.Field('longitude'),
                coreapi.Field('latitude'),
                coreapi.Field('name'),
                coreapi.Field('description'),
                coreapi.Field('email'),
                coreapi.Field('phone'),
                coreapi.Field('crops'),
                coreapi.Field('address'),
                coreapi.Field('geom_point'),
                coreapi.Field('geom_polygon'),
                coreapi.Field('primary_purpose'),
                coreapi.Field('members'),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields

class ResourceViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post', 'put']:
            extra_fields = [
                coreapi.Field('resource_status'),
                coreapi.Field('resource_name'),
                coreapi.Field('category'),
                coreapi.Field('date_created'),
                coreapi.Field('return_date'),
                coreapi.Field('garden'),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


#Javier Martín - 04/12/2021

# Create your views here.

# GARDENS
# 1 of 2: request for all ['GET']
class GardenView(APIView):
    schema =GardenViewSchema()
    def get(self,request):

        if request.method == 'GET':
            gardens = Garden.objects.all()
            garden_serializer = GardenSerializer(gardens, many=True)
            return JsonResponse(garden_serializer.data, safe=False)
            # 'safe=False' for objects serialization
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
        resource_serializer = GardenSerializer(data=resource_data) 
        if resource_serializer.is_valid(): 
            resource_serializer.save() 
            return JsonResponse(resource_serializer.data) 
        return JsonResponse(resource_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 