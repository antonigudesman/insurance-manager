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
        type_ = self.cleaned_data.get('type')
        t1_ee = self.cleaned_data.get('t1_ee')
        t2_ee = self.cleaned_data.get('t2_ee')
        t3_ee = self.cleaned_data.get('t3_ee')
        t4_ee = self.cleaned_data.get('t4_ee')
        t1_gross = self.cleaned_data.get('t1_gross')
        t2_gross = self.cleaned_data.get('t2_gross')
        t3_gross = self.cleaned_data.get('t3_gross')
        t4_gross = self.cleaned_data.get('t4_gross')
        t1_ercdhp = self.cleaned_data.get('t1_ercdhp')
        t2_ercdhp = self.cleaned_data.get('t2_ercdhp')
        t3_ercdhp = self.cleaned_data.get('t3_ercdhp')
        t4_ercdhp = self.cleaned_data.get('t4_ercdhp')
        in_ded_single = self.cleaned_data.get('in_ded_single')
        in_max_single = self.cleaned_data.get('in_max_single')
        in_ded_family = self.cleaned_data.get('in_ded_family')
        in_max_family = self.cleaned_data.get('in_max_family')
        out_ded_single = self.cleaned_data.get('out_ded_single')
        out_max_single = self.cleaned_data.get('out_max_single')
        out_ded_family = self.cleaned_data.get('out_ded_family')
        out_max_family = self.cleaned_data.get('out_max_family')
        out_coin = self.cleaned_data.get('out_coin')
        hsa = self.cleaned_data.get('hsa')
        hra = self.cleaned_data.get('hra')

        # add custom validation rules 
        if t1_ee > t1_gross and t1_gross:
            self._errors['t1_ee'] = ErrorList([''])
            self._errors['t1_gross'] = ErrorList([''])
            raise forms.ValidationError("Employee Only tier: Gross cost must be higher than employee cost.")

        if t2_ee > t2_gross and t2_gross:
            self._errors['t2_ee'] = ErrorList([''])
            self._errors['t2_gross'] = ErrorList([''])
            raise forms.ValidationError("Employee & Spouse tier: Gross cost must be higher than employee cost.")

        if t3_ee > t3_gross and t3_gross:
            self._errors['t3_ee'] = ErrorList([''])
            self._errors['t3_gross'] = ErrorList([''])
            raise forms.ValidationError("Employee & Child(ren) tier: Gross cost must be higher than employee cost.")

        if t4_ee > t4_gross and t4_gross:
            self._errors['t4_ee'] = ErrorList([''])
            self._errors['t4_gross'] = ErrorList([''])
            raise forms.ValidationError("Family tier: Gross cost must be higher than employee cost.")

        if in_ded_single > 7150 and in_ded_single:
            self._errors['in_ded_single'] = ErrorList([''])
            raise forms.ValidationError("The deductible and out-of-pocket limit for an individual is $7,150.")

        if in_max_single > 7150 and in_max_single:
            self._errors['in_max_single'] = ErrorList([''])
            raise forms.ValidationError("The deductible and out-of-pocket limit for an individual is $7,150.")

        if in_ded_family > 14300 and in_ded_family:
            self._errors['in_ded_family'] = ErrorList([''])
            raise forms.ValidationError("The deductible and out-of-pocket limit for a family is $14,300.")

        if in_max_family > 14300 and in_max_family:
            self._errors['in_max_family'] = ErrorList([''])
            raise forms.ValidationError("The deductible and out-of-pocket limit for a family is $14,300.")

        if (type_ == 'HMO' or type_ == 'EPO') and (out_ded_single or out_ded_family or out_max_single or out_max_family or \
            out_coin):
            self._errors['out_ded_single'] = ErrorList([''])
            self._errors['out_ded_family'] = ErrorList([''])
            self._errors['out_max_single'] = ErrorList([''])
            self._errors['out_max_family'] = ErrorList([''])
            self._errors['out_coin'] = ErrorList([''])            
            raise forms.ValidationError("HMO or EPO plans should not have out-of-network benefits.")

        if not (hsa or hra) and (t1_ercdhp or t2_ercdhp or t3_ercdhp or t4_ercdhp):
            self._errors['t1_ercdhp'] = ErrorList([''])
            self._errors['t2_ercdhp'] = ErrorList([''])
            self._errors['t3_ercdhp'] = ErrorList([''])
            self._errors['t4_ercdhp'] = ErrorList([''])        
            raise forms.ValidationError("Only plans paired with a HRA or HSA can have employer-funding.")

        if in_ded_single > out_ded_single and out_ded_single:
            self._errors['in_ded_single'] = ErrorList([''])
            self._errors['out_ded_single'] = ErrorList([''])
            raise forms.ValidationError("Out-of-network single deductible should be greater than the in-network single deductible.")

        if in_ded_family > out_ded_family and out_ded_family:
            self._errors['in_ded_family'] = ErrorList([''])
            self._errors['out_ded_family'] = ErrorList([''])
            raise forms.ValidationError("Out-of-network family deductible should be greater than the in-network family deductible.")

        if in_max_single > out_max_single and out_max_single:
            self._errors['in_max_single'] = ErrorList([''])
            self._errors['out_max_single'] = ErrorList([''])
            raise forms.ValidationError("Out-of-network single maximum should be greater than the in-network single maximum.")

        if in_max_family > out_max_family and out_max_family:
            self._errors['in_max_family'] = ErrorList([''])
            self._errors['out_max_family'] = ErrorList([''])
            raise forms.ValidationError("Out-of-network family maximum should be greater than the in-network family maximum.")

        return self.cleaned_data


class DentalForm(ModelForm):
    class Meta:
        model = Dental
        exclude = []

    def clean(self):
        t1_ee = self.cleaned_data.get('t1_ee')
        t1_gross = self.cleaned_data.get('t1_gross')
        t2_ee = self.cleaned_data.get('t2_ee')
        t2_gross = self.cleaned_data.get('t2_gross')
        t3_ee = self.cleaned_data.get('t3_ee')
        t3_gross = self.cleaned_data.get('t3_gross')
        t4_ee = self.cleaned_data.get('t4_ee')
        t4_gross = self.cleaned_data.get('t4_gross')
        type_ = self.cleaned_data.get('type')
        out_ded_single = self.cleaned_data.get('out_ded_single')
        out_ded_family = self.cleaned_data.get('out_ded_family')
        out_max = self.cleaned_data.get('out_max')
        out_max_ortho = self.cleaned_data.get('out_max_ortho')
        out_prev_coin = self.cleaned_data.get('out_prev_coin')
        out_basic_coin = self.cleaned_data.get('out_basic_coin')
        out_major_coin = self.cleaned_data.get('out_major_coin')
        out_ortho_coin = self.cleaned_data.get('out_ortho_coin')        

        # add custom validation rules 
        if t1_ee > t1_gross and t1_gross:
            self._errors['t1_ee'] = ErrorList([''])
            self._errors['t1_gross'] = ErrorList([''])
            raise forms.ValidationError("Single Employee Cost should be less than Single Gross Cost.")

        if t2_ee > t2_gross and t2_gross:
            self._errors['t2_ee'] = ErrorList([''])
            self._errors['t2_gross'] = ErrorList([''])
            raise forms.ValidationError("Employee & Spouse Cost should be less than Employee & Spouse Gross Cost.")

        if t3_ee > t3_gross and t3_gross:
            self._errors['t3_ee'] = ErrorList([''])
            self._errors['t3_gross'] = ErrorList([''])
            raise forms.ValidationError("Employee & Child(ren) Cost should be less than Employee & Child(ren) Gross Cost")

        if t4_ee > t4_gross and t4_gross:
            self._errors['t4_ee'] = ErrorList([''])
            self._errors['t4_gross'] = ErrorList([''])
            raise forms.ValidationError("Family Cost should be less than Family Gross Cost.")

        if type_ == 'DMO' and (out_ded_single or out_ded_family or out_max or out_max_ortho or \
            out_prev_coin or out_basic_coin or out_major_coin or out_ortho_coin):
            self._errors['out_ded_single'] = ErrorList([''])
            self._errors['out_ded_family'] = ErrorList([''])
            self._errors['out_max'] = ErrorList([''])
            self._errors['out_max_ortho'] = ErrorList([''])
            self._errors['out_prev_coin'] = ErrorList([''])
            self._errors['out_basic_coin'] = ErrorList([''])
            self._errors['out_major_coin'] = ErrorList([''])
            self._errors['out_ortho_coin'] = ErrorList([''])            
            raise forms.ValidationError("DMO plans should not have out-of-network benefits.")

        return self.cleaned_data


class VisionForm(ModelForm):
    class Meta:
        model = Vision
        exclude = []

    def clean(self):
        t1_ee = self.cleaned_data.get('t1_ee')
        t1_gross = self.cleaned_data.get('t1_gross')
        t2_ee = self.cleaned_data.get('t2_ee')
        t2_gross = self.cleaned_data.get('t2_gross')
        t3_ee = self.cleaned_data.get('t3_ee')
        t3_gross = self.cleaned_data.get('t3_gross')
        t4_ee = self.cleaned_data.get('t4_ee')
        t4_gross = self.cleaned_data.get('t4_gross')

        # add custom validation rules 
        if t1_ee > t1_gross and t1_gross:
            self._errors['t1_ee'] = ErrorList([''])
            self._errors['t1_gross'] = ErrorList([''])
            raise forms.ValidationError("Single Employee Cost should be less than Single Gross Cost.")

        if t2_ee > t2_gross and t2_gross:
            self._errors['t2_ee'] = ErrorList([''])
            self._errors['t2_gross'] = ErrorList([''])
            raise forms.ValidationError("Employee & Spouse Cost should be less than Employee & Spouse Gross Cost.")

        if t3_ee > t3_gross and t3_gross:
            self._errors['t3_ee'] = ErrorList([''])
            self._errors['t3_gross'] = ErrorList([''])
            raise forms.ValidationError("Employee & Child(ren) Cost should be less than Employee & Child(ren) Gross Cost.")

        if t4_ee > t4_gross and t4_gross:
            self._errors['t4_ee'] = ErrorList([''])
            self._errors['t4_gross'] = ErrorList([''])
            raise forms.ValidationError("Family Cost should be less than Family Gross Cost.")

        return self.cleaned_data


class LifeForm(ModelForm):
    class Meta:
        model = Life
        exclude = []

    def clean(self):
        type_ = self.cleaned_data.get('type')
        multiple = self.cleaned_data.get('multiple')
        multiple_max = self.cleaned_data.get('multiple_max')
        flat_amount = self.cleaned_data.get('flat_amount')

        # add custom validation rules 
        if type_ == 'Multiple of Salary' and flat_amount:
            self._errors['flat_amount'] = ErrorList([''])
            raise forms.ValidationError("If plan type is Multiple of Salary, Flat Amount value should be left blank.")

        if type_ == 'Flat Amount' and (multiple_max or multiple):
            self._errors['multiple'] = ErrorList([''])
            self._errors['multiple_max'] = ErrorList([''])
            raise forms.ValidationError("If plan type is Flat Amount, Multiple and Multiple Max values should be left blank.")

        return self.cleaned_data


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

    def clean(self):
        spousal_surcharge = self.cleaned_data.get('spousal_surcharge')
        spousal_surcharge_amount = self.cleaned_data.get('spousal_surcharge_amount')
        tobacco_surcharge = self.cleaned_data.get('tobacco_surcharge')
        tobacco_surcharge_amount = self.cleaned_data.get('tobacco_surcharge_amount')

        # add custom validation rules 
        if not spousal_surcharge and spousal_surcharge_amount:
            self._errors['spousal_surcharge'] = ErrorList([''])
            raise forms.ValidationError("If Spousal Surcharge Amount is provided, the Require Spousal Surcharge dropdown must be set to Yes.")

        if not tobacco_surcharge and tobacco_surcharge_amount:
            self._errors['tobacco_surcharge'] = ErrorList([''])
            raise forms.ValidationError("If Tobacco Surcharge Amount is provided, the Require Tobacco Surcharge dropdown must be set to Yes.")

        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    # current = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'class': 'form-control'}))
    new = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'class': 'form-control'}))
    confirm = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'class': 'form-control'}))

    def clean(self):
        # current = self.cleaned_data.get('current')
        new = self.cleaned_data.get('new')
        confirm = self.cleaned_data.get('confirm')

        # add custom validation rules 
        if new != confirm:
            raise forms.ValidationError("Password is not correct!")
            
        return self.cleaned_data
