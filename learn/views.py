from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
from django.utils import timezone

from learn.models import Step, Course
from user.models import StepProgress, LessonProgress, CourseEnrollment, Award 
from learn.models import find_siblings_step, find_next_lesson

import logging

class CurrentLesson(View):
    def get(self, request, **kwargs):
        user = request.user
        lessons = Course.objects.get(id=kwargs['course_id']).course_plan.all().values_list('lesson', flat=True)
        if lesson := user.lessonprogress_set.filter(completed=False, lesson__in=lessons).first():
            return redirect(lesson.lesson.url)
        else:
            messages.info(request, "This course is complete.")
        return redirect('home')

class UpdateProgress(View):
    def get(self, request, **kwargs):
        now = timezone.now()
        step = Step.objects.get(pk=kwargs['step_id'])
        data = {'step': step, 'user': request.user}
        update_generic_progress(data, now, StepProgress)
        prev, next = find_siblings_step(step)
        if next:
            messages.info(request, f"Step {step.title} completed.")
        else:
            data = {'lesson': step.get_parent(), 'user': request.user}
            update_generic_progress(data, now, LessonProgress)
            if next := find_next_lesson(step.get_parent()):
                awards = check_for_awards(page=step.get_parent(), user=request.user)
                if awards:
                    messages.success(request, f"Congratulations! You earned the {awards[0].badge} badge.")
                messages.info(request, f"Starting next lesson {next.title}")
            else:
                next = step.get_parent().get_parent()
                data = {'course': next, 'user': request.user}
                update_generic_progress(data, now, CourseEnrollment)
                messages.success(request, f"Course {next.title} complete")
        return redirect(next.url)
    
def update_generic_progress(data, now, objmodel):
    obj = objmodel.objects.get(**data)
    if not obj.completed:
        obj.completed = True
        obj.completion_date = now
        lock = check_for_dependencies(obj)
        logging.debug(f"Lock: {lock} for {obj}")
        obj.save()
        return True
    return False

def check_for_dependencies(obj):
    # Unlock any lessons that depend on this one
    try:
        obj.locks.all()
    except AttributeError:
        return None
    for lesson in obj.locks.all():
        lesson.lessonprogress_set.filter(user=obj.user).update(locked=False)
    return True

def check_for_awards(page, user):
    lesson = page.lesson
    if requirements := lesson.badgerequirement_set.all():
        awards = []
        # Check is user has these already
        for requirement in requirements:
            award, created = Award.objects.get_or_create(badge=requirement.badge, user=user)
            if created:
                awards.append(award)
    else:
        return None
    