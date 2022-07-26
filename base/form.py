from dataclasses import fields
from pyexpat import model
from django import forms
from .models import Room
from django.contrib.auth.models import User


class RoomForm(forms.ModelForm):
    class Meta:
        model= Room
        fields ='__all__'
        
class UserForm(forms.ModelForm):
    class Meta:
        model= User
        fields=['username','email']
        