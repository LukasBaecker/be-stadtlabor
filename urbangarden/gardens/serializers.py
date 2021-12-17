from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import Garden,Resource

#Garden
class GardenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garden
        geo_field = ['geom_point', 'geom_polygon']
        fields = ('__all__')
        

# Resource
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['resource_id', 'resource_status', 'resource_name', 
                'category', 'date_created', 'return_date', 'garden'
                  #'lender ', #'borrower '
        ]

         