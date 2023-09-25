from django.contrib.auth.models import User
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

# forms to allow easy user input


# used in submitForm api
class AreaRatingForm(forms.ModelForm):
    class Meta:
        model = Area
        exclude = ('name','country', 'city', 'borough', 'image')

# used in createArea api
class AreaForm(forms.ModelForm):
    class Meta: 
        model = Area
        fields = '__all__' 

# used in submitDescription api
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('description', 'id')