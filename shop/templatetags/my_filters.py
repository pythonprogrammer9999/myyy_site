from math import floor

from django import template

register = template.Library()


@register.filter(name='convert_play')
def convert_play(value):
    hours = int(floor(value / 3600))
    minutes = int(floor(value - hours * 3600) / 60)
    seconds = int(value - hours * 3600 - minutes * 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'
