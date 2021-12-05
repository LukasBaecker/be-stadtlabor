from rest_framework import serializers
from .models import Garden,Resource

#Garden
class GardenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garden
        fields = ['garden_id', 'longitude', 'latitude',
                  'name', 'description', 'email', 
                  'phone', 'crops', 'address', 
                  #'geom_point', #'geom_polygon'
        ]

# Resource
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['resource_id', 'resource_status', 'resource_name', 
                'category', 'date_created', 'return_date', 'garden'
                  #'lender ', #'borrower '
        ]

         