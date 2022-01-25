from rest_framework import serializers
from crops.models import Crop

class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'

class CropPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = ['gardens']
