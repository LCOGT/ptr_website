from django.db import models

from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.fields import RichTextField

from home.blocks import BodyBlock

class HomePage(Page):
    summary = RichTextField("optional summary/teaser", blank=True)
    content = StreamField(BodyBlock)
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Homepage image",
    )

    content_panels = Page.content_panels + [
        FieldPanel('featured_image'),
        FieldPanel('summary'),
        FieldPanel('content'),
    ]


@register_snippet
class ContentCategory(models.Model):
    name = models.CharField(max_length=30)
    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "content category"
        verbose_name_plural = 'content categories'