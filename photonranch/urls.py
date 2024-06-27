from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from rest_framework import routers

from search import views as search_views
from user.views import Enrol, Login, logout_view, UserProfileApi
from learn.views import UpdateProgress

# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    path("progress/<int:step_id>/update/", UpdateProgress.as_view(), name="update_progress"),
    path("enrol/", Enrol.as_view(), name="enrol"),
    path("account/login/", Login.as_view(), name="login"),
    path("account/logout/", logout_view, name="logout"),
    path("api/user/profile/", UserProfileApi.as_view()),
    path("", include(wagtail_urls)),
]
