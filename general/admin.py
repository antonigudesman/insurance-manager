from django.contrib import admin
from django import forms
from django.forms.utils import ErrorList

from .models import *


class EmployerAdmin(admin.ModelAdmin):
    list_display = ['name','broker','industry1','industry2','industry3',
                    'state','formatted_size','nonprofit','med_count','den_count',
                    'vis_count', 'life_count','std_count','ltd_count']
    search_fields = ('name','broker')
    list_filter = ('broker',)
    change_form_template = 'admin/change_form_employer.html'
    fields = ('name', 'broker', 'industry1', 'state', 'industry2', 'size', 'industry3')

    def get_queryset(self, request):
        qs = super(EmployerAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(broker=group)
            
        return qs

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        plans = []
        for model in [Medical, Dental, Vision, Life, STD, LTD, Strategy]:
            for item in model.objects.filter(employer_id=object_id):
                url = '/admin/general/{}/{}/change/'.format(model.__name__.lower(), item.pk)
                if model == Strategy:
                    plans.append([item.employer.name, url, model.__name__])
                else:
                    plans.append([item.title, url, model.__name__])

        extra_context['plans'] = plans

        return super(EmployerAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def formatted_size(self, obj):
        try:
            return '{:,.0f}'.format(obj.size)
        except Exception as e:
            return '-'
    formatted_size.short_description = 'Size'
    formatted_size.admin_order_field = 'size' 


class MedicalForm(forms.ModelForm):
    class Meta:
        model = Medical
        fields = '__all__'

    def clean(self):
        t1_ee = self.cleaned_data.get('t1_ee')
        t1_gross = self.cleaned_data.get('t1_gross')

        # add custom validation rules 
        if t1_ee > t1_gross:
            self._errors['t1_ee'] = ErrorList([''])
            self._errors['t1_gross'] = ErrorList([''])
            raise forms.ValidationError("Single Employee Cost should be less than Single Gross Cost!")

        return self.cleaned_data


class MedicalAdmin(admin.ModelAdmin):
    list_display = ['title','employer','type','formatted_ded_single',
                    'formatted_max_single','formatted_coin']
    search_fields = ('employer__name', 'title',)
    list_filter = ('type',)
    form = MedicalForm
    fields = ('title', 'employer')

    def get_queryset(self, request):
        qs = super(MedicalAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(employer__broker=group)
            
        return qs

    def formatted_ded_single(self, obj):
        try:
            return '${:,.0f}'.format(obj.in_ded_single)
        except Exception as e:
            return '-'
    formatted_ded_single.short_description = 'IN Deductible (Ind)'
    formatted_ded_single.admin_order_field = 'in_ded_single' 

    def formatted_max_single(self, obj):
        try:
            return '${:,.0f}'.format(obj.in_max_single)
        except Exception as e:
            return '-'
    formatted_max_single.short_description = 'IN Maximum (Ind)'
    formatted_max_single.admin_order_field = 'in_max_single' 

    def formatted_coin(self, obj):
        if obj.in_coin != None:
            return '{:,.0f}%'.format(obj.in_coin)
    formatted_coin.short_description = 'IN Coinsurances'
    formatted_coin.admin_order_field = 'in_coin' 


class DentalAdmin(admin.ModelAdmin):
    list_display = ['title','employer','type','formatted_ded_single',
                    'formatted_in_max','formatted_in_max_ortho']
    search_fields = ('employer__name', 'title',)
    list_filter = ('type',)
    fields = ('title', 'employer')

    def get_queryset(self, request):
        qs = super(DentalAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(employer__broker=group)
            
        return qs

    def formatted_ded_single(self, obj):
        try:
            return '${:,.0f}'.format(obj.in_ded_single)
        except Exception as e:
            return '-'
    formatted_ded_single.short_description = 'IN Deductible (Ind)'
    formatted_ded_single.admin_order_field = 'in_ded_single' 

    def formatted_in_max(self, obj):
        try:
            return '${:,.0f}'.format(obj.in_max)
        except Exception as e:
            return '-'
    formatted_in_max.short_description = 'IN Maximum (Ind)'
    formatted_in_max.admin_order_field = 'in_max' 

    def formatted_in_max_ortho(self, obj):
        try:
            return '${:,.0f}'.format(obj.in_max_ortho)
        except Exception as e:
            return '-'
    formatted_in_max_ortho.short_description = 'IN Ortho Max (PP)'
    formatted_in_max_ortho.admin_order_field = 'in_max_ortho' 


class VisionAdmin(admin.ModelAdmin):
    list_display = ['title','employer','formatted_exam_copay','formatted_lenses_copay',
                    'formatted_frames_allowance','formatted_contacts_allowance']
    search_fields = ('employer__name', 'title',)
    fields = ('title', 'employer')
    
    def get_queryset(self, request):
        qs = super(VisionAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(employer__broker=group)
            
        return qs

    def formatted_exam_copay(self, obj):
        try:
            return '${:,.0f}'.format(obj.exam_copay)
        except Exception as e:
            return '-'
    formatted_exam_copay.short_description = 'Exam Copay'
    formatted_exam_copay.admin_order_field = 'exam_copay' 

    def formatted_lenses_copay(self, obj):
        try:
            return '${:,.0f}'.format(obj.lenses_copay)
        except Exception as e:
            return '-'
    formatted_lenses_copay.short_description = 'Lenses Copay'
    formatted_lenses_copay.admin_order_field = 'lenses_copay' 

    def formatted_frames_allowance(self, obj):
        try:
            return '${:,.0f}'.format(obj.frames_allowance)
        except Exception as e:
            return '-'
    formatted_frames_allowance.short_description = 'Frames Allowance'
    formatted_frames_allowance.admin_order_field = 'frames_allowance' 

    def formatted_contacts_allowance(self, obj):
        try:
            return '${:,.0f}'.format(obj.contacts_allowance)
        except Exception as e:
            return '-'
    formatted_contacts_allowance.short_description = 'Contacts Allowance'
    formatted_contacts_allowance.admin_order_field = 'contacts_allowance' 


class LifeAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'type', 'multiple', 
                    'formatted_multiple_max', 'formatted_flat_amount', 'add', 'cost_share']
    search_fields = ('employer__name',)
    fields = ('title', 'employer')
    
    def get_queryset(self, request):
        qs = super(LifeAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(employer__broker=group)
            
        return qs

    def formatted_multiple_max(self, obj):
        try:
            return '${:,.0f}'.format(obj.multiple_max)
        except Exception as e:
            return '-'
    formatted_multiple_max.short_description = 'Multiple Max'
    formatted_multiple_max.admin_order_field = 'multiple_max' 

    def formatted_flat_amount(self, obj):
        try:
            return '${:,.0f}'.format(obj.flat_amount)
        except Exception as e:
            return '-'
    formatted_flat_amount.short_description = 'Flat Amount'
    formatted_flat_amount.admin_order_field = 'flat_amount' 


class STDAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'waiting_days', 'duration_weeks', 
                    'formatted_percentage', 'formatted_weekly_max', 'cost_share']
    search_fields = ('employer__name', 'title',)
    fields = ('title', 'employer')
    
    def get_queryset(self, request):
        qs = super(STDAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(employer__broker=group)
            
        return qs

    def formatted_percentage(self, obj):
        try:
            return '{:.0f}%'.format(obj.percentage)
        except Exception as e:
            return '-'
    formatted_percentage.short_description = 'Percentage'
    formatted_percentage.admin_order_field = 'percentage' 

    def formatted_weekly_max(self, obj):
        try:
            return '${:,.0f}'.format(obj.weekly_max)
        except Exception as e:
            return '-'
    formatted_weekly_max.short_description = 'Weekly Max'
    formatted_weekly_max.admin_order_field = 'weekly_max' 


class LTDAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'waiting_weeks', 
                    'formatted_percentage', 'formatted_monthly_max', 'cost_share']
    search_fields = ('employer__name', 'title',)
    fields = ('title', 'employer')
    
    def get_queryset(self, request):
        qs = super(LTDAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(employer__broker=group)
            
        return qs

    def formatted_percentage(self, obj):
        try:
            return '{:.0f}%'.format(obj.percentage)
        except Exception as e:
            return '-'
    formatted_percentage.short_description = 'Percentage'
    formatted_percentage.admin_order_field = 'percentage' 

    def formatted_monthly_max(self, obj):
        try:
            return '${:,.0f}'.format(obj.monthly_max)
        except Exception as e:
            return '-'
    formatted_monthly_max.short_description = 'Monthly Max'
    formatted_monthly_max.admin_order_field = 'monthly_max' 


class StrategyAdmin(admin.ModelAdmin):
    list_display = ['employer',]
    search_fields = ('employer__name', 'title',)
    fields = ('employer', 'offer_vol_life')
    

    def get_queryset(self, request):
        qs = super(StrategyAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(employer__broker=group)
            
        return qs

admin.site.register(Employer, EmployerAdmin)
admin.site.register(Life, LifeAdmin)
admin.site.register(STD, STDAdmin)
admin.site.register(LTD, LTDAdmin)
admin.site.register(Strategy, StrategyAdmin)
admin.site.register(Vision, VisionAdmin)
admin.site.register(Dental, DentalAdmin)
admin.site.register(Medical, MedicalAdmin)
