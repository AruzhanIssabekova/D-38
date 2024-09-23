from django import template
from django.utils.safestring import mark_safe, SafeText
from django.utils.html import escape


register = template.Library()

# @register.filter(is_safe=True)
def currency(value, name='руб.'):
    return '%1.2f %s' % (value, name)

register.filter('currency', currency)

@register.simple_tag
def lst(sep, *args):
    return mark_safe('%s (итого <strong>%s</strong>)' % (sep.join(args), len(args)))


@register.inclusion_tag('tags/ulist.html')
def ulist(*args):
    return {'items': args}