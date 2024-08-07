from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import FieldPanel
from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem

from user.models import Badge, BadgeRequirement
from user.views import user_progress_summary, user_progress


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
        path('progress/', user_progress_summary, name='user_progress_all'),
        path('progress/<int:user_id>/', user_progress, name='user_progress')
    ]

@hooks.register('register_admin_menu_item')
def register_user_process_item():
    return MenuItem('User Progress', reverse('user_progress_all'), icon_name='group')

register_snippet(BadgeViewSet)
register_snippet(BadgeRequirementViewSet)