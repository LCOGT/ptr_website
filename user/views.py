from django import forms
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.views import View

from learn.models import Course, Lesson, Step
from user.models import CourseEnrollment, LessonProgress, StepProgress

class EnrolForm(forms.Form):
    course_id = forms.IntegerField(widget=forms.HiddenInput)

    def clean_course_id(self):
        course_id = self.cleaned_data['course_id']
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise forms.ValidationError("Invalid course ID")
        return course_id

    def enrol(self, user):
        course = Course.objects.get(id=self.cleaned_data['course_id'])
        # create enrollement records for course, lessons and steps
        ce, created = CourseEnrollment.objects.get_or_create(course=course, user=user)
        for lesson in Lesson.objects.filter(courseplan__course=course):
            lp, created = LessonProgress.objects.get_or_create(lesson=lesson, user=user)
            for step in Step.objects.filter(lessonplan__lesson=lesson):
                sp, created = StepProgress.objects.get_or_create(step=step, user=user)
        return course

class Enrol(View):
    form_class = EnrolForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            course = form.enrol(request.user)
            messages.success(request, f"You have been enrolled on to {course.title}.")
            return redirect(reverse('learn:course', args=[course.slug]))
