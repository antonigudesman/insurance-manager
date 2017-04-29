from django import template

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
