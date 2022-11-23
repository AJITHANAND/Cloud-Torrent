
from .models import *
from django import forms


class Register(forms.ModelForm):
    class Meta:
        model = user
        fields = ['name', 'email', 'password']
