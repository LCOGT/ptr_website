from django.contrib.auth.models import User
from django.db import models

from learn.models import Course, Lesson, Step

class Badge(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Badge image",
    )

    def __str__(self):
        return self.name

class BadgeRequirement(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    lesson = models.ManyToManyField(Lesson)
    message = models.TextField()

    def __str__(self):
        return f"{self.badge} requirements"

class Award(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    awarded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.badge}"

    class Meta:
        unique_together = ('badge', 'user')
    
class CourseEnrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completion_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        unique_together = ('course', 'user')

class LessonProgress(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    last_update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.lesson}"

    class Meta:
        unique_together = ('lesson', 'user')
        verbose_name = 'Lesson Progress'
        verbose_name_plural = 'Lesson Progresses'


class StepProgress(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completion_date = models.DateField(null=True, blank=True)
    task_info = models.TextField(blank=True) 

    def __str__(self):
        return f"{self.user} - {self.step}"

    class Meta:
        unique_together = ('step', 'user')
        verbose_name = 'Step Progress'
        verbose_name_plural = 'Step Progresses'