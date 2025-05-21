from __future__ import annotations
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from videos.views import ProgressViewSet, VideoViewSet
from users.views import logout

# ---------------------------------------------------------------------------
# DRF-Router (API v1)
# ---------------------------------------------------------------------------
router = DefaultRouter()
router.register(r"videos", VideoViewSet)
router.register(r"progress", ProgressViewSet, basename="progress")

# ---------------------------------------------------------------------------
# URL-Patterns
# ---------------------------------------------------------------------------
urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # API
    path("api/", include(router.urls)),
    path("api/auth/", include("djoser.urls.jwt")),  # Hier nur einmal einfügen
    path("api/auth/", include("users.urls")),
   # path("api/auth/logout/", logout, name="logout"),

    # RQ-Dashboard
    path("django-rq/", include("django_rq.urls")),
]

# ---------------------------------------------------------------------------
# Statische Medien nur im DEBUG-Modus direkt aus Django dienen
# ---------------------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Debug Toolbar
    import debug_toolbar  # noqa: WPS433 – nur dev

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
