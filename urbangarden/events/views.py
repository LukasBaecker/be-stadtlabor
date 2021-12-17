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
                coreapi.Field('title'),
                coreapi.Field('description'),
                coreapi.Field('name'),
                coreapi.Field('description'),
                coreapi.Field('venue'),
                coreapi.Field('date'),
                coreapi.Field('duration'),
                coreapi.Field('garden'),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


#Nivedita Vee
@api_view(['GET', 'POST', 'DELETE'])
def event_list(request):
    schema =EventViewSchema()
    if request.method == 'GET':
        events = Event.objects.all()
        event_serializer = EventSerializer(events, many=True)
        return JsonResponse(event_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        events = Event.objects.all()
        events_data = JSONParser().parse(request)
        event_serializer = EventSerializer(events, many=True)
        tutorial_serializer = EventSerializer(data=events_data)
        if event_serializer.is_valid():
            event_serializer.save()
            return JsonResponse(event_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Event.objects.all().delete()
        return JsonResponse({'message': '{} Events were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])

def event_detail(request, pk):
    schema =EventViewSchema()
    try: 
        event = Event.objects.get(pk=pk) 
    except Event.DoesNotExist: 
        return JsonResponse({'message': 'The event does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        event_serializer = EventSerializer(event) 
        return JsonResponse(event_serializer.data) 
 
    elif request.method == 'PUT': 
        event_data = JSONParser().parse(request) 
        event_serializer = EventSerializer(event, data=event_data) 
        if event_serializer.is_valid(): 
            event_serializer.save() 
            return JsonResponse(event_serializer.data) 
        return JsonResponse(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        event.delete() 
        return JsonResponse({'message': 'Event was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    