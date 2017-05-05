from django import forms
from django.forms import ModelForm
from django.forms.utils import ErrorList

from .models import *

class MedicalForm(ModelForm):
    class Meta:
        model = Medical
        exclude = []

    def clean_pcp_ded_apply(self):
        return self.parse_none('pcp_ded_apply')

    def clean_sp_ded_apply(self):
        return self.parse_none('sp_ded_apply')

    def clean_er_ded_apply(self):
        return self.parse_none('er_ded_apply')

    def clean_uc_ded_apply(self):
        return self.parse_none('uc_ded_apply')

    def clean_lx_ded_apply(self):
        return self.parse_none('lx_ded_apply')

    def clean_ip_ded_apply(self):
        return self.parse_none('ip_ded_apply')

    def clean_op_ded_apply(self):
        return self.parse_none('op_ded_apply')

    def clean_rx1_ded_apply(self):
        return self.parse_none('rx1_ded_apply')

    def clean_rx2_ded_apply(self):
        return self.parse_none('rx2_ded_apply')

    def clean_rx3_ded_apply(self):
        return self.parse_none('rx3_ded_apply')

    def clean_rx4_ded_apply(self):
        return self.parse_none('rx4_ded_apply')

    def parse_none(self, prop):
        data = self.cleaned_data[prop]
        if data == 'None':
            return None
        return data

    def clean(self):
        t1_ee = self.cleaned_data.get('t1_ee')
        t1_gross = self.cleaned_data.get('t1_gross')
        t2_ee = self.cleaned_data.get('t2_ee')
        t2_gross = self.cleaned_data.get('t2_gross')
        t3_ee = self.cleaned_data.get('t3_ee')
        t3_gross = self.cleaned_data.get('t3_gross')
        t4_ee = self.cleaned_data.get('t4_ee')
        t4_gross = self.cleaned_data.get('t4_gross')

        in_ded_single = self.cleaned_data.get('in_ded_single')
        in_max_single = self.cleaned_data.get('in_max_single')

        # add custom validation rules 
        if t1_ee > t1_gross and t1_gross:
            self._errors['t1_ee'] = ErrorList([''])
            self._errors['t1_gross'] = ErrorList([''])
            raise forms.ValidationError("Single Employee Cost should be less than Single Gross Cost!")

        if t2_ee > t2_gross and t2_gross:
            self._errors['t2_ee'] = ErrorList([''])
            self._errors['t2_gross'] = ErrorList([''])
            raise forms.ValidationError("Employee & Spouse Cost should be less than Employee & Spouse Gross Cost!")

        if t3_ee > t3_gross and t3_gross:
            self._errors['t3_ee'] = ErrorList([''])
            self._errors['t3_gross'] = ErrorList([''])
            raise forms.ValidationError("Employee & Child(ren) Cost should be less than Employee & Child(ren) Gross Cost!")

        if t4_ee > t4_gross and t4_gross:
            self._errors['t4_ee'] = ErrorList([''])
            self._errors['t4_gross'] = ErrorList([''])
            raise forms.ValidationError("Family Cost should be less than Family Gross Cost!")

        if in_ded_single > 6550 and in_ded_single:
            self._errors['in_ded_single'] = ErrorList([''])
            raise forms.ValidationError("Maximum deductible for singles must be less than $6,550")

        if in_max_single > 6550 and in_max_single:
            self._errors['in_max_single'] = ErrorList([''])
            raise forms.ValidationError("Maximum annual out-of-pocket for singles must be less than $6,550!")

        return self.cleaned_data


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
