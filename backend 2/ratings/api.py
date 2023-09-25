from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .models import *
from .forms import *

from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from .serializers import *

from django.http import HttpResponseRedirect

from django.http import QueryDict   

@api_view(['POST'])
def createArea(request):
    # fill in new area data into form along with image
    form = request.data
    area_form = AreaForm(request.data, request.FILES)

    if area_form.is_valid(): # if form is valid
        # first look for an area that has that name if it does then display message there's already that area and show them. 
        try: # try seeing if there exists an area with identical values
            area = Area.objects.get(name = form['name'], country = form['country'], city = form['city'], borough = form['borough'])
            serializer = GetAreaId(area, many = False)
        except:
            area = False

        if area == False: # if area found
            new_area = area_form.save()
            id = new_area.id
            context = {
                'validation_errors': False,
                'area_exists': False,
                'area_id': id
            }
            return Response(context, status = status.HTTP_201_CREATED)
        else: # if area with that name already exists notify client
            context = {
                'validation_errors': False,
                'area_exists': True,
                'area_id': serializer.data
            }
            return Response(context, status = status.HTTP_409_CONFLICT)
        
    else: # if there are validaion errors return them
        context = {
            'area_exists': False,
            'validation_errors': True,
            'area_form_errors': area_form.errors 
        }
        return Response(context, status = status.HTTP_400_BAD_REQUEST)
    

# get area list
@api_view(['GET'])
def getAreas(request, areaName):
    # get the areas with areaName as name
    areas = Area.objects.filter(name = areaName)
    if areas:
        # serialze the data in json format
        areas_serialized = GetArea(areas, many = True)
        # get the ratings for this area. 
        context = {
            'areas': areas_serialized.data,
        }
        # send the area
        return Response(context, status = status.HTTP_200_OK)
    else:
        # otherwise send 400 status
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def submitDescription(request):
    # get area from area id in request
    area_id = request.data['area_id']
    area = Area.objects.get(id = area_id)
    # get user from user id in request.
    user_id = request.data['user']['user_id']
    user = User.objects.get(id = user_id)
    # validate rating form 
    rating_form = RatingForm(request.data)
    # if form is valida save form and add area and author as FK.
    if rating_form.is_valid():
        print(rating_form)
        new_rating = rating_form.save(commit=False)
        new_rating.area = area
        # add user as FK
        new_rating.author = user
        new_rating.save() 
    else:
        # send eroors
        context= {
            'errors': rating_form.errors
        }
        return Response(context, status = status.HTTP_204_NO_CONTENT)
    
    return Response(status = status.HTTP_201_CREATED)


@api_view(['POST'])
def submitForm(request):
    # get rating form and validate using form
    rating_form = AreaRatingForm(request.data)
    rating = request.data['rating']
    # if form is valid increment rating using self function in models. 
    if rating_form.is_valid():
        areaId = request.data['id']
        area_ = Area.objects.get(id = areaId) 
        area_.process_rating(rating)
        area_.save()
        return Response(status = status.HTTP_201_CREATED)
    else:
        return Response(status = status.HTTP_304_NOT_MODIFIED)
   
@api_view(['POST'])
def deleteRating(request):
    rating_form = AreaRatingForm(request.data)
    rating = request.data['rating']
    # if form is valid delete rating from database using self function in models
    if rating_form.is_valid():
        areaId = request.data['id']
        area_ = Area.objects.get(id = areaId) 
        area_.delete_rating(rating)
        area_.save()
        return Response(status = status.HTTP_201_CREATED)
    else:
        return Response(status = status.HTTP_304_NOT_MODIFIED) 
