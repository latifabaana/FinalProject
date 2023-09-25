from rest_framework import serializers
from .models import *

# all serializers to format data before it gets returned to the client.

# used in getAreas
class GetDescription(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        depth = 2

# used in getAreas api
class GetArea(serializers.ModelSerializer):
    rating_item = GetDescription(many = True)
    class Meta:
        model = Area
        fields = ['name', 'rating_item', 'cig_but_count', 
                  'swearing_count', 'litter_count', 
                  'homeless_sightings', 'image', 'id', 'country', 'city', 'borough']


# used in createArea api
class GetAreaId(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id',]

