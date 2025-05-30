"""videos/viewsets.py – REST API für Filme & Wiedergabefortschritt"""
from __future__ import annotations

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from .models import Video, WatchProgress
from .serializers import ProgressSerializer, VideoSerializer

__all__ = [
    "VideoViewSet",
    "ProgressViewSet",
]

CACHE_TTL: int = getattr(settings, "CACHE_TTL", 60 * 15)


@method_decorator(cache_page(CACHE_TTL), name="list")
@method_decorator(cache_page(CACHE_TTL), name="retrieve")
class VideoViewSet(viewsets.ModelViewSet):
    """Komplette CRUD-API für *Video*, GET-Endpunkte werden gecacht."""

    serializer_class = VideoSerializer

    def get_queryset(self):
        if self.action == "list":
            return Video.objects.filter(is_trailer=False)
        return Video.objects.all()

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WatchProgress.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        obj, _ = WatchProgress.objects.update_or_create(
            user=request.user,
            video_id=data.get("video"),
            defaults={
                "position": data.get("position", 0),
                "duration": data.get("duration", 0),
            },
        )
        return Response(self.get_serializer(obj).data, status=status.HTTP_201_CREATED)

    http_method_names = ["get", "post", "head", "options"]


class TrailerList(ListAPIView):
    serializer_class = VideoSerializer
    queryset = Video.objects.filter(is_trailer=True, duration__lte=240)
    permission_classes = []
