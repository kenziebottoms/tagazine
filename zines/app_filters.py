from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='words')
@stringfilter
def words(value, arg):
    return value.split(' ')