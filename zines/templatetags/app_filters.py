from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='lastWord')
@stringfilter
def lastWord(value):
    return value.split(' ')[0].strip()
def length(value):
    return len(value)