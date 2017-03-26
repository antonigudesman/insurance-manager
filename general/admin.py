from django.contrib import admin
from .models import *


class EmployerAdmin(admin.ModelAdmin):
    list_display = [item.name for item in Employer._meta.fields if item.name != 'id']

    def get_queryset(self, request):
        qs = super(EmployerAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(broker=group)
            
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

    def get_queryset(self, request):
        qs = super(STDAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(employer__broker=group)
            
        return qs


class LTDAdmin(admin.ModelAdmin):
    list_display = [item.name for item in LTD._meta.fields if item.name != 'id']

    def get_queryset(self, request):
        qs = super(LTDAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(employer__broker=group)
            
        return qs


class StrategyAdmin(admin.ModelAdmin):
    list_display = [item.name for item in Strategy._meta.fields if item.name != 'id']

    def get_queryset(self, request):
        qs = super(StrategyAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(employer__broker=group)
            
        return qs


class VisionAdmin(admin.ModelAdmin):
    list_display = [item.name for item in Vision._meta.fields if item.name != 'id']

    def get_queryset(self, request):
        qs = super(VisionAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(employer__broker=group)
            
        return qs


class DentalAdmin(admin.ModelAdmin):
    list_display = [item.name for item in Dental._meta.fields if item.name != 'id']

    def get_queryset(self, request):
        qs = super(DentalAdmin, self).get_queryset(request)
        group = request.user.groups.first().name

        if group != 'bnchmrk':
            qs = qs.filter(employer__broker=group)
            
        return qs


class MedicalAdmin(admin.ModelAdmin):
    list_display = [item.name for item in Medical._meta.fields if item.name != 'id']

    def get_queryset(self, request):
        qs = super(MedicalAdmin, self).get_queryset(request)
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
