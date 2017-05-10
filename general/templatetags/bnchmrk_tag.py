from django import template
from django.contrib.auth.models import Group 

register = template.Library()

@register.filter
def parse_boolean(value): # Only one argument.
    """Converts a string into boolean"""
    if value == None or value == 'None':
        return None
    elif value == True or value == "True":
        return True
    return False

@register.filter
def parse_none(value): # Only one argument.
    """Converts a string into none"""
    if value == None:
        return None
    else:
        return value        

@register.filter
def replace_slash(value): # Only one argument.
    if value == 'MEDICALRX':
        return 'Medical & Rx'
    elif value == 'DENTAL':
        return 'Dental'
    elif value == 'LIFE':
        return 'Life'
    elif value == 'VISION':
        return 'Vision'
    elif value == 'STRATEGY':
        return 'Strategy'
    else:
        return value

@register.filter(name='has_group') 
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all() 