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


admin.site.register(Employer, EmployerAdmin)
admin.site.register(Life, LifeAdmin)
admin.site.register(STD, STDAdmin)
