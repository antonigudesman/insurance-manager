from django.contrib import admin
from django import forms
from django.forms.utils import ErrorList

from .models import *


class EmployerAdmin(admin.ModelAdmin):
    list_display = ['name','broker','industry1','industry2','industry3',
                    'state','size','nonprofit','med_count','den_count','vis_count',
                    'life_count','std_count','ltd_count']
    search_fields = ('name','broker')
    list_filter = ('broker',)
    change_form_template = 'admin/change_form_employer.html'

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

    def formatted_max_single(self, obj):
        try:
            return '${:,.0f}'.format(obj.in_max_single)
        except Exception as e:
            return '-'

    def formatted_coin(self, obj):
        if obj.in_coin != None:
            return '{:,.0f}%'.format(obj.in_coin)


class DentalAdmin(admin.ModelAdmin):
    list_display = ['title','employer','type','in_ded_single',
                    'in_max','in_max_ortho']
    search_fields = ('employer__name', 'title',)
    list_filter = ('type',)

    def get_queryset(self, request):
        qs = super(DentalAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(employer__broker=group)
            
        return qs


class VisionAdmin(admin.ModelAdmin):
    list_display = ['title','employer','exam_copay','lenses_copay',
                    'frames_allowance','contacts_allowance']
    search_fields = ('employer__name', 'title',)

    def get_queryset(self, request):
        qs = super(VisionAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(employer__broker=group)
            
        return qs


class LifeAdmin(admin.ModelAdmin):
    list_display = [item.name for item in Life._meta.fields if item.name != 'id']
    search_fields = ('employer__name',)

    def get_queryset(self, request):
        qs = super(LifeAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(employer__broker=group)
            
        return qs


class STDAdmin(admin.ModelAdmin):
    list_display = [item.name for item in STD._meta.fields if item.name != 'id']
    search_fields = ('employer__name', 'title',)

    def get_queryset(self, request):
        qs = super(STDAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(employer__broker=group)
            
        return qs


class LTDAdmin(admin.ModelAdmin):
    list_display = [item.name for item in LTD._meta.fields if item.name != 'id']
    search_fields = ('employer__name', 'title',)

    def get_queryset(self, request):
        qs = super(LTDAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(employer__broker=group)
            
        return qs


class StrategyAdmin(admin.ModelAdmin):
    list_display = ['employer',]
    search_fields = ('employer__name', 'title',)

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
