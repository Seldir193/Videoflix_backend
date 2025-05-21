"""videos/viewsets.py – REST API für Filme & Wiedergabefortschritt"""
from __future__ import annotations

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models      import Video, WatchProgress
from .serializers import ProgressSerializer, VideoSerializer

__all__ = [
    "VideoViewSet",
    "ProgressViewSet",
]

CACHE_TTL: int = getattr(settings, "CACHE_TTL", 60 * 15)

# ---------------------------------------------------------------------------
# 🎬  Videos – öffentlich lesbar, Bearbeitung nur authentifiziert
# ---------------------------------------------------------------------------

@method_decorator(cache_page(CACHE_TTL), name="list")
@method_decorator(cache_page(CACHE_TTL), name="retrieve")
class VideoViewSet(viewsets.ModelViewSet):
    """Komplette CRUD-API für *Video*, GET-Endpunkte werden gecacht."""

    queryset         = Video.objects.all()  # Ordering kommt aus Model.Meta
    serializer_class = VideoSerializer

    def get_permissions(self):  # noqa: D401
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

# ---------------------------------------------------------------------------
# ⏯  Wiedergabefortschritt – pro User & Video eindeutig
# ---------------------------------------------------------------------------

class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class   = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # noqa: D401
        return WatchProgress.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):  # noqa: D401
        data = request.data
        obj, _ = WatchProgress.objects.update_or_create(
            user     = request.user,
            video_id = data.get("video"),
            defaults = {
                "position": data.get("position", 0),
                "duration": data.get("duration", 0),
            },
        )
        return Response(self.get_serializer(obj).data, status=status.HTTP_201_CREATED)

    # Keine Detail-Updates nötig – nur Position wird überschrieben → PATCH unnötig
    http_method_names = ["get", "post", "head", "options"]











