from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import Garden,Resource, ResourceBorrowing

#Garden
class GardenSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Garden
        geo_field = 'geom_point'
        fields = '__all__'
       

#Nearest Gardens
class NearestGardenSerializer(GeoFeatureModelSerializer):

    distance = serializers.CharField(default='0')

    class Meta:
        model = Garden
        geo_field = 'geom_point'
        fields = '__all__'
        #read_only_fields = ['distance']

        

# Resource
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__' #Changed to solve the description's bug


# ResourceBorrowing
class ResourceBorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceBorrowing
        fields = '__all__'
