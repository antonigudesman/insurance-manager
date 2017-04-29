from django import forms
from django.forms import ModelForm

from .models import *

class MedicalForm(ModelForm):
    class Meta:
        model = Medical
        exclude = []


class DentalForm(ModelForm):
    class Meta:
        model = Dental
        exclude = []


class VisionForm(ModelForm):
    class Meta:
        model = Vision
        exclude = []


class LifeForm(ModelForm):
    class Meta:
        model = Life
        exclude = []


class STDForm(ModelForm):
    class Meta:
        model = STD
        exclude = []


class LTDForm(ModelForm):
    class Meta:
        model = LTD
        exclude = []


class StrategyForm(ModelForm):
    class Meta:
        model = Strategy
        exclude = []
