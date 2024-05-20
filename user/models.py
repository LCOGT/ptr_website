from django.contrib.auth.models import User
from django.db import models

from learn.models import Course, Lesson, Step

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='badges/')

    def __str__(self):
        return self.name
    
class CourseEnrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completion_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        unique_together = ('course', 'user')
        verbose_name = ' Course Enrollment'
        verbose_name_plural = 'Course Enrollments'


class LessonProgress(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    last_update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        unique_together = ('lesson', 'user')
        verbose_name = ' Lesson Progress'
        verbose_name_plural = 'Lesson Progresses'


class StepProgress(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completion_date = models.DateField(null=True, blank=True)
    task_info = models.TextField(blank=True) 

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        unique_together = ('step', 'user')
        verbose_name = 'Step Progress'
        verbose_name_plural = 'Step Progresses'