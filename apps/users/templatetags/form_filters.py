from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Add a CSS class to the form field."""
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='split')
def split(value, delimiter):
    """Split a string by a delimiter."""
    return value.split(delimiter)