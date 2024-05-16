from django import forms
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

from learn.models import Course

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
        course.enrol(user)

class Enrol(View):
    form_class = EnrolForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.enrol(request.user)
            course = Course.objects.get(id=form.cleaned_data['course_id'])
            messages.success(request, f"You have been enrolled on to {course.title}.")
            return redirect(reverse('learn:course', args=[course.slug]))
