from django import template
from django.contrib.auth.models import Group 
import json

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
def parse_list(llist, idx): # Only one argument.
    """Converts a string into none"""
    llist = json.loads(llist)
    if idx >= len(llist):
        return ''
    return llist[idx]

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


@register.filter
def format_benefit(value): # Only one argument.
    if value == 'MEDICALRX':
        return 'Medical / Rx'
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


@register.filter
def get_percent(dn, db): # Only one argument.
    return dn * 100.0 / db
    
@register.filter(name='has_group') 
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all() 


@register.filter
def json_dump(llist): # Only one argument.
    return json.dumps(llist)


@register.filter(name='logo_img')
def logo_img(user):
    img_name = 'bnchmrk'
    group = user.groups.first().name.lower()
    if group in ['nfp', 'namely']:
        img_name = group
    return '/static/img/{}_logo.png'.format(img_name)


@register.filter
def permitted(user):
    group = user.groups.first().name.lower()
    return not group in ['nfp', 'namely']


@register.filter
def broker(user):
    return user.groups.first().name.lower()
