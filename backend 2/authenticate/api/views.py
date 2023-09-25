from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .forms import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import status

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def signup(request):
    # get the inputs from the form and put it into a form to validate
    user_form = UserForm(data=request.data['signup'])
    # if form content is valid
    if user_form.is_valid():
        print('form is valid')
        # save the form as user instance 
        user = user_form.save()
        user.save()
        registered = True
    # if user form is not valid, send the form back back to the sign up page, for them to try again
        context = {
            'registered': registered,
            'form-errors': user_form.errors
        }
        if user:
            return Response(context, status=status.HTTP_201_CREATED) 
    else:
        # if not registered send user form errors
        registered = False
        context = {
            'registered': registered,
            'form-errors': user_form.errors
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)  
        


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]
    return Response(routes)

