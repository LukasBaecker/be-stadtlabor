from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.schemas import AutoSchema
from .serializers import EventSerializer
from .models import Event
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
import jwt 
from events.models import Event
from events.serializers import EventSerializer
from rest_framework.decorators import api_view

import coreapi
from rest_framework.schemas import AutoSchema


#CoreAPI schema -> Brian Pondi 

class EventViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post', 'put']:
            extra_fields = [
                coreapi.Field(
                    name = 'title',
                    required = True,
                    description= 'Event title: Creating a bountiful garden',
                    type='string'), 
                coreapi.Field(
                    name = 'description',
                    required = True,
                    description= 'Chracteristics, details, aim (etc): In the event we will discover ...',
                    type='string'),
                coreapi.Field(
                    name = 'venue',
                    required = True,
                    description= 'Place where the event takes place: Aasee park',
                    type='string'),
                coreapi.Field(
                    name = 'date',
                    required = True,
                    description= '2021-12-16 T12:00:00Z',
                    type='string'),
                coreapi.Field(
                    name = 'duration',
                    required = True,
                    description= '02:00:00',
                    type='string'),
                coreapi.Field(
                    name = 'garden',
                    required = True,
                    description= 'Garden id: 1 or 2 or 3 ...',
                    type='integer'),   
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


#Nivedita Vee

class EventView(APIView):
    schema =EventViewSchema()
    def get(self,request):
   
       if request.method == 'GET':
        events = Event.objects.all()
        event_serializer = EventSerializer(events, many=True)
        return JsonResponse(event_serializer.data, safe=False)
        # 'safe=False' for objects serialization
   
 
 
class EventDetailView(APIView):
    schema =EventViewSchema()
    def get(self,request,pk):
      
        event = Event.objects.get(pk=pk)
        event_serializer = EventSerializer(event) 
        return JsonResponse(event_serializer.data) 
 
    
   
    def put(self,request,pk):
     token = request.COOKIES.get('jwt')
     if not token:
            raise AuthenticationFailed('Unauthenticated!')
     try:
            event = Event.objects.get(pk=pk) 
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
     except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

     event_data = JSONParser().parse(request) 
     event_serializer = EventSerializer(event, data=event_data) 
     if event_serializer.is_valid(): 
            event_serializer.save() 
            return JsonResponse(event_serializer.data) 
     return JsonResponse(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
     token = request.COOKIES.get('jwt')
     if not token:
            raise AuthenticationFailed('Unauthenticated!')
     try:
            event = Event.objects.get(pk=pk) 
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
     except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

     event.delete() 
     return JsonResponse({'message': 'Event was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
class EventDetailViewPost(APIView):
     schema =EventViewSchema()

     def post(self,request): 
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        event_data = JSONParser().parse(request) 
        event_serializer = EventSerializer(data=event_data) 
        if event_serializer.is_valid(): 
            event_serializer.save() 
            return JsonResponse(event_serializer.data) 
        return JsonResponse(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
  



    
    
    
