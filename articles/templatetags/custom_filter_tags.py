from django import template
from articles.models import ImageModel, TextModel

register = template.Library()


@register.filter
def check_image(value):
    return type(value) == ImageModel


@register.filter
def check_text(value):
    return type(value) == TextModel


@register.filter
def capitalize_all(value):
    return value.upper()


@register.filter
def shrink(value):
    if len(value) < 30:
        return value
    return value[:29]


@register.filter
def get_index(item, lst):
    return lst.index(item)


@register.filter
def multiply(value):
    value = int(value)
    return str(value * 100)