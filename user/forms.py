from django import forms

from learn.models import Course, Lesson, Step
from user.models import CourseEnrollment, LessonProgress

class EnrolForm(forms.Form):
    course_id = forms.IntegerField(widget=forms.HiddenInput)

    def clean_course_id(self):
        course_id = self.cleaned_data['course_id']
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise forms.ValidationError("Invalid course ID")
        return course_id

    def enrol(self, user, force=False):
        course = Course.objects.get(id=self.cleaned_data['course_id'])
        # create enrollement records for course, lessons and steps
        ce, ce_created = CourseEnrollment.objects.get_or_create(course=course, user=user)
        if ce_created and not force:
            return course, ce_created
        for lesson in Lesson.objects.filter(courseplan__course=course):
            lp, created = LessonProgress.objects.get_or_create(lesson=lesson, user=user, locked=locked)
            if lesson.depends_on and created:
                lp.locked = True
                lp.save()
            for step in Step.objects.filter(lessonplan__lesson=lesson):
                sp, created = StepProgress.objects.get_or_create(step=step, user=user)
        return course, ce_created
    
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username or not password:
            raise forms.ValidationError("Please enter a username and password")
        return cleaned_data