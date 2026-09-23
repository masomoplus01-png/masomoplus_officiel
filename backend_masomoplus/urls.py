from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("accounts.urls")),
    path("academic/", include("academic.urls")),
    path("api/academic/", include("academic.urls")),
    path("api/documents/", include("documents.urls")),
    path("api/authors/", include("authors.urls")),
    path("api/moderation/", include("moderation.urls")),
    path("api/interactions/", include("interactions.urls")),
    path("api/analytics/", include("analytics.urls")),
    path("api/projets/", include("collaboration.urls")),
    path("api/notifications/", include("notifications.urls")),
    path("api/support/", include("support.urls")),
    path("api/actualites/", include("actualites.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

