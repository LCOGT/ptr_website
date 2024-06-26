from django import template
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db.models import Prefetch
from wagtail.rich_text import expand_db_html

from user.models import CourseEnrollment, LessonProgress, StepProgress
from learn.models import LessonPlan

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

@register.simple_tag
def progress(user, lesson):
    try:
        if LessonProgress.objects.get(lesson=lesson, user=user).completed:
            return 100
        else:
            step_ids = LessonPlan.objects.filter(lesson=lesson).values_list('step_id', flat=True)
            steps = StepProgress.objects.filter(user=user, step__id__in=step_ids)
            completed = steps.filter(completed=True).count()
            return f"{completed / steps.count() * 100:.0f}"

    except LessonProgress.DoesNotExist:
        return False
    
@register.simple_tag
def has_requisites(user, step):
    return StepProgress.objects.filter(step=step, user=user)