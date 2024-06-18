from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import FieldPanel

from user.models import Badge, BadgeRequirement


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

register_snippet(BadgeViewSet)
register_snippet(BadgeRequirementViewSet)