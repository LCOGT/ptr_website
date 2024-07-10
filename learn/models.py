from django.db import models
from django import forms
from django.db.models import Subquery, OuterRef
from django.apps import apps
from django.urls import reverse

from wagtail.models import Page, Orderable
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, PageChooserPanel, InlinePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.search import index

from home.blocks import BodyBlock

class LearnIndexPage(Page):
    content = StreamField(BodyBlock)

    content_panels = Page.content_panels + [
        FieldPanel('content')
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        lessonprogress = apps.get_model('user', 'LessonProgress')
        courseenrollment = apps.get_model('user', 'CourseEnrollment')
        courses = CoursePlan.objects.all()
        course_list = []
        if not request.user.is_authenticated:
            # Ugly code so the template can handle the same data structure
            # Better would be to annotate the queryset with the progress
            for course in Course.objects.all():
                data = {'complete': None, 'total': None, 'course': course, 'enrolled': None}
                course_list.append(data)
        else:
            for course in Course.objects.all():
                courseplan = courses.filter(course=course)
                complete = lessonprogress.objects.filter(user=request.user, completed=True, lesson=Subquery(courseplan.values('lesson'))).count()
                total = courseplan.count()
                percent = f"{complete / total * 100:.0f}" if total > 0 else 0
                enrolled = courseenrollment.objects.filter(user=request.user, course=course).exists()
                data = {'complete': complete, 'total': total, 'course': course, 'enrolled': enrolled, 'percent': percent}
                print(data)
                course_list.append(data)
        context['courses'] = course_list
        return context
    
    parent_page_types = ['home.HomePage']


class Course(Page):
    parent_page_types = ['learn.LearnIndexPage']
    subpage_types = ['learn.Lesson']
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    teaser = models.CharField("Optional teaser", max_length=250, blank=True)
    content = StreamField(BodyBlock)
    category = ParentalManyToManyField('home.ContentCategory', blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('teaser'),
        index.SearchField('content'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('featured_image'),
        FieldPanel('teaser'),
        FieldPanel('content'),
        FieldPanel('category', widget=forms.CheckboxSelectMultiple),
        InlinePanel('course_plan', label="Course Lessons"),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        lessonprogress = apps.get_model('user', 'LessonProgress')
        lessonprog = lessonprogress.objects.filter(lesson=OuterRef('pk'), user=request.user)
        context['lessons'] = self.course_plan.all().annotate(progress=Subquery(lessonprog.values('completed')[:1]))
        print(context['lessons'][0].__dict__)
        if request.user.is_authenticated:
            context['enrolled'] = Course.objects.filter(courseenrollment__user=request.user).exists()
        return context
    

class Lesson(Page):
    parent_page_types = ['learn.Course']
    subpage_types = ['learn.Step']
    content = StreamField(BodyBlock)
    depends_on =  models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='locks'
    )

    content_panels = Page.content_panels + [
        FieldPanel('content'),
        PageChooserPanel('depends_on', 'learn.Lesson'),
        InlinePanel('lesson_plan', label="Steps"),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('content'),
    ]

    def get_context(self, request):
        stepprogress = apps.get_model('user', 'StepProgress')
        stepsprog = stepprogress.objects.filter(step=OuterRef('pk'), user=request.user)
        steps = self.lesson_plan.all().annotate(progress=Subquery(stepsprog.values('completed')[:1]))
        context = super().get_context(request)
        context['breadcrumbs'] = breadcrumbs(self)
        context['steps'] = steps
        context['course'] = self.get_parent()
        if request.user.is_authenticated:
            context['enrolled'] = Course.objects.filter(courseenrollment__user=request.user).exists()
        return context


class Step(Page):
    parent_page_types = ['learn.Lesson']
    content = StreamField(BodyBlock)

    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('content'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['breadcrumbs'] = breadcrumbs(self)
        context['course'] = self.get_parent().get_parent()
        context['prev'], context['next'] = find_siblings_step(step=self)
        if not context['next']:
            if next := find_next_lesson(self.get_parent()):
                context['next'] = next
                context['nextlesson'] = True
            else:
                context['next'] = self.get_parent().get_parent()
                context['coursecomplete'] = True
        if request.user.is_authenticated:
            context['enrolled'] = Course.objects.filter(courseenrollment__user=request.user).exists()
            if context['enrolled']:
                context['nexturl'] = reverse('update_progress', args=[self.id])
            else:
                context['nexturl'] = context['next'].url
            if self.stepprogress_set.filter(user=request.user).exists():
                context['completed'] = self.stepprogress_set.get(user=request.user).completed
        return context


class CoursePlan(Orderable):
    course = ParentalKey(Course, on_delete=models.CASCADE, related_name='course_plan')
    lesson = models.ForeignKey('learn.Lesson', on_delete=models.CASCADE)

    panels = [
        FieldPanel('lesson'),
    ]

class LessonPlan(Orderable):
    lesson = ParentalKey(Lesson, on_delete=models.CASCADE, related_name='lesson_plan')
    step = models.ForeignKey('learn.Step', on_delete=models.CASCADE)

    panels = [
        FieldPanel('step'),
    ]

def breadcrumbs(page):
    breadcrumbs = []
    
    while page.get_parent() is not None:
        if page.is_root() or page.get_parent().title == 'Learn':
            break
        # To avoid including self in breadcrumbs
        page = page.get_parent()
        breadcrumbs.append(page)

    breadcrumbs.reverse()
    return breadcrumbs

def find_siblings_step(step):
    plan = list(step.get_parent().lesson.lesson_plan.all().values_list('step__pk', flat=True))
    place = plan.index(step.pk)
    if place == 0 and len(plan) > 1:
        next = plan[1]
        prev = None
    elif place == len(plan) - 1:
        next = None
        prev = plan[place - 1]
    elif len(plan) == 1:
        next = None
        prev = None
    else:
        next = plan[place + 1]
        prev = plan[place - 1]
    if next:
        next = Step.objects.get(pk=next)
    if prev:
        prev = Step.objects.get(pk=prev)
    return prev, next
    
def find_next_lesson(lesson):
    plan = list(lesson.get_parent().course.course_plan.all().values_list('lesson__pk', flat=True))
    place = plan.index(lesson.pk)
    if place == len(plan) - 1:
        next = None
    else:
        next = plan[place + 1]
    if next:
        next = Lesson.objects.get(pk=next)
    return next
