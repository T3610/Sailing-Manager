from datetime import datetime
from django import template

register = template.Library()

@register.filter
def timestamp(value):
    try:
        return value.timestamp()
    except:
        return ''