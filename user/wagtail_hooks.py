from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import FieldPanel
from django.urls import path
from wagtail import hooks

from user.models import Badge, BadgeRequirement
from user.views import user_progress


class BadgeViewSet(SnippetViewSet):
    model = Badge

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("image")
    ]

class BadgeRequirementViewSet(SnippetViewSet):
    model = BadgeRequirement

    panels = [
        FieldPanel("badge"),
        FieldPanel("lesson"),
        FieldPanel("message")
    ]

@hooks.register('register_admin_urls')
def register_useradmin_url():
    return [
        path('users/progress/', user_progress, name='user_progress'),
    ]

register_snippet(BadgeViewSet)
register_snippet(BadgeRequirementViewSet)