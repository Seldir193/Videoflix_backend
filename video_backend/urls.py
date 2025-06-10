from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from videos.views import ProgressViewSet, VideoViewSet, TrailerList
from users.views import activate
from video_backend.views import health_check



router = DefaultRouter()
router.register(r"progress", ProgressViewSet, basename="progress")
router.register(r"videos", VideoViewSet, basename="videos")

urlpatterns = [
    path("admin/", admin.site.urls),

    # API routes
    re_path(r"^api/", include(router.urls)),
    re_path(r"^api/auth/", include("djoser.urls")),
    re_path(r"^api/auth/", include("djoser.urls.jwt")),

    # Password reset flow
    path("api/auth/password_reset/", auth_views.PasswordResetView.as_view(), name="password-reset"),
    path("api/auth/password_reset_done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("api/auth/password_reset_confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("api/auth/password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # Activation + trailers
    path("activate/<uidb64>/<token>/", activate, name="account-activate"),
    path("api/trailers/", TrailerList.as_view(), name="trailer-list"),

    # Django-RQ dashboard
    path("django-rq/", include("django_rq.urls")),

    path('api/health/', health_check, name='health-check'),
]

# Static/media + debug toolbar
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]




