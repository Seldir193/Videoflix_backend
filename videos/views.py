"""API views for videos and watch‑progress."""

from __future__ import annotations

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Video, WatchProgress
from .serializers import ProgressSerializer, VideoSerializer

__all__ = [
    "VideoViewSet",
    "ProgressViewSet",
    "TrailerList",
]

CACHE_TTL: int = getattr(settings, "CACHE_TTL", 60 * 15)


@method_decorator(cache_page(CACHE_TTL), name="retrieve")
class VideoViewSet(viewsets.ModelViewSet):
    """Video CRUD API (auth required)."""

    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # noqa: D401
        """Return trailers or full catalog depending on action."""
        if self.action == "list":
            return Video.objects.filter(is_trailer=False)
        return Video.objects.all()


class ProgressViewSet(viewsets.ModelViewSet):
    """Track per‑user playback progress."""

    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):  # noqa: D401
        """Return progress entries for current user."""
        return WatchProgress.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):  # noqa: D401
        """Upsert progress (called from player)."""
        video_id = request.data.get("video")
        position = request.data.get("position")
        duration = request.data.get("duration")

        progress, _ = WatchProgress.objects.update_or_create(
            user=request.user,
            video_id=video_id,
            defaults={"position": position, "duration": duration},
        )
        return Response(
            self.get_serializer(progress).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, url_path="get_progress", methods=["get"])
    def get_progress(self, request):  # noqa: D401
        """Return stored progress for given *video* (or zeros)."""
        video_id = request.query_params.get("video")

        obj = WatchProgress.objects.filter(
            user=request.user,
            video_id=video_id,
        ).first()

        if not obj:
            return Response({"position": 0, "duration": 0})

        return Response(
            {
                "id": obj.id,
                "position": obj.position,
                "duration": obj.duration,
            }
        )


class TrailerList(ListAPIView):
    """Read‑only list of short trailers (≤ 240 s)."""

    serializer_class = VideoSerializer
    queryset = Video.objects.filter(is_trailer=True, duration__lte=240)
    permission_classes = [IsAuthenticated]
