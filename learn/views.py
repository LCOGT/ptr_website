from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
from django.utils import timezone

from learn.models import Step
from user.models import StepProgress, LessonProgress, CourseEnrollment, Award, BadgeRequirement

class UpdateProgress(View):
    def get(self, request, *args, **kwargs):
        now = timezone.now()
        step = Step.objects.get(pk=kwargs['step_id'])
        data = {'step': step, 'user': request.user}
        update_generic_progress(data, now, StepProgress)
        
        if next := step.get_next_sibling():
            messages.info(request, f"Step {step.title} completed.")
        else:
            data = {'lesson': step.get_parent(), 'user': request.user}
            update_generic_progress(data, now, LessonProgress)
            if next := step.get_parent().get_next_sibling():
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
        obj.save()
        return True
    return False

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
    