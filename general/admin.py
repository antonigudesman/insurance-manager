from django.contrib import admin
from .models import *


class EmployerAdmin(admin.ModelAdmin):
    list_display = [item.name for item in Employer._meta.fields if item.name != 'id']


class LifeAdmin(admin.ModelAdmin):
    list_display = [item.name for item in Life._meta.fields if item.name != 'id']
    search_fields = ('employer__name',)


class STDAdmin(admin.ModelAdmin):
    list_display = [item.name for item in STD._meta.fields if item.name != 'id']

admin.site.register(Employer, EmployerAdmin)
admin.site.register(Life, LifeAdmin)
admin.site.register(STD, STDAdmin)
