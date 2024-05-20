from django import template
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from wagtail.rich_text import expand_db_html

from user.models import CourseEnrollment, LessonProgress

register = template.Library()

@register.filter
def betterhtml(html):
    return mark_safe(expand_db_html(html))

@register.filter
def is_enrolled(user, course):
    return user.is_authenticated and CourseEnrollment.objects.filter(course=course, user=user).exists()

@register.filter
def pre_requisite(user, lesson):
    return lesson.depends_on is None or LessonProgress.objects.filter(lesson=lesson.depends_on, user=user, completed=True).exists()