from django.db import models
from django import forms

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
        course_list = Course.objects.live().order_by('-go_live_at')
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
        InlinePanel('course_plan', label="Course Plan"),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        context['lessons'] = self.course_plan.all()
        return context
    

class Lesson(Page):
    parent_page_types = ['learn.Course']
    subpage_types = ['learn.Step']
    content = StreamField(BodyBlock)
    depends_on =  models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = Page.content_panels + [
        FieldPanel('content'),
        PageChooserPanel('depends_on', 'learn.Lesson'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('content'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['breadcrumbs'] = breadcrumbs(self)
        context['steps'] = Step.objects.live().descendant_of(self)
        context['course_title'] = self.get_parent().title
        return context
    

class CoursePlan(Orderable):
    page = ParentalKey(Course, on_delete=models.CASCADE, related_name='course_plan')
    lesson = models.ForeignKey('learn.Lesson', on_delete=models.CASCADE)

    panels = [
        FieldPanel('lesson'),
    ]

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
        return context
    
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