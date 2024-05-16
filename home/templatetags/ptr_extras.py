from django import template
from django.utils.safestring import mark_safe
from wagtail.rich_text import expand_db_html

import logging

logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
def betterhtml(html):
    return mark_safe(expand_db_html(html))