from django.urls import path, include
from rest_framework.schemas import get_schema_view
from . import views
from . import api
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('submitDescription', api.submitDescription, name = 'submitDescription'),
    path('getArea/<str:areaName>', api.getAreas, name = 'getArea'),
    path('createArea', api.createArea, name = 'createArea'),
    path('submitForm', api.submitForm, name ='submitForm'),
    path('deleteRating', api.deleteRating, name ='deleteRating'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)