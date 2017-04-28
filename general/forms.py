from django import forms
from django.forms import ModelForm

from .models import *

class DentalForm(ModelForm):
    class Meta:
        model = Dental
        exclude = []
