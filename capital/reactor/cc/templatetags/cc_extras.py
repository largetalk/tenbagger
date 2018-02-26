from django import template

register = template.Library()

@register.filter(name='key')
def key(d,key_name):
    value = None
    try:
        value = d[key_name]
    except KeyError:
        value = None
    return value
