from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='insert_linebreaks')
def insert_linebreaks(value, char_count):
    char_count = int(char_count)
    return mark_safe('\n'.join(value[i:i+char_count] for i in range(0, len(value), char_count)))
