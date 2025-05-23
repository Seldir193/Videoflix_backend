from __future__ import annotations
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path, include, path  # Füge 'path' hier hinzu
from rest_framework.routers import DefaultRouter

from videos.views import ProgressViewSet, VideoViewSet
# from users.views import logout

from users import views 
from django.contrib.auth import views as auth_views
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
#from rest_framework.authtoken.views import obtain_auth_token
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
    re_path(r'^api/', include(router.urls)),  # Video und Progress API Endpoints
    re_path(r'^api/auth/', include('djoser.urls')),  # Djoser Auth-Routen (Registrierung, Login, Aktivierung)
    re_path(r'^api/auth/', include('djoser.urls.jwt')),  # JWT-Authentifizierung mit Djoser
    #path('api/auth/', include('djoser.urls.authtoken')), 
    
    #path('api/auth/users/reset_password/', views.password_reset, name='password-reset'),
   # path('api/auth/users/reset_password_confirm/', views.password_reset_confirm, name='password-reset-confirm'),
    
    
    path('api/auth/password_reset/', auth_views.PasswordResetView.as_view(), name='password-reset'),

    # Standard-Ansicht nach dem Absenden der E-Mail
    path('api/auth/password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    # Standard-Ansicht zur Passwortbestätigung
    path('api/auth/password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Standard-Ansicht nach erfolgreichem Zurücksetzen des Passworts
    path('api/auth/password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    
    path('auth/activate/<uidb64>/<token>/', views.activate, name='account-activate'),

    
    
    # RQ-Dashboard für Redis Queue
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