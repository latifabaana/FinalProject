import factory
from django.test import TestCase
from django.conf import settings
from django.core.files import File

from django.contrib.auth.models import User

from .models import *

# creates model factories for each model with dummy data already inserted. 

class AreaFactory(factory.django.DjangoModelFactory):
    name = 'manor park'
    country = 'united kingdom'
    city = 'london'
    borough = 'newham'
    image = ''
    homeless_sightings = 0
    litter_count = 0
    swearing_count = 0
    cig_but_count = 0

    class Meta:
        model = Area

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

class RatingFactory(factory.django.DjangoModelFactory):
    area = factory.SubFactory(AreaFactory)
    author = factory.SubFactory(UserFactory)
    description = 'this is the best area ever!'

    class Meta:
        model = Rating

