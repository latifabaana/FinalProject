from django.contrib.auth.models import User
from django import forms
from authenticate.models import *
from django.contrib.auth.forms import UserCreationForm

from django.core import validators
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator

def validate_email(email):
        lower_email = email.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise forms.ValidationError("This email already exists")
        return lower_email

# user form
class UserForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', validators=[validate_email]) 
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
