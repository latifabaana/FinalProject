import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponse
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *

# test serializers
class SerializerTest(APITestCase):
    
    # test getDescription serializer
    def test_GetDescription(self):
        rating = RatingFactory.create()
        ratingSerializer = GetDescription(instance = rating)
        rating_data = ratingSerializer.data
        self.assertEqual(set(rating_data.keys()), set(['id','area', 'author', 'description']))

    # test getDescription serializer
    def test_GetArea(self):
        area = AreaFactory.create()
        areaSerializer = GetArea(instance = area)
        area_data = areaSerializer.data
        self.assertEqual(set(area_data.keys()), set(['name','city', 'image', 'swearing_count', 'rating_item', 'country', 'cig_but_count', 'litter_count', 'borough', 'homeless_sightings', 'id']))

    # test GetAreaId serializer
    def test_GetAreaId(self):
        area = AreaFactory.create()
        areaSerializer = GetAreaId(instance = area)
        area_data = areaSerializer.data
        self.assertEqual(set(area_data.keys()), set(['id']))