from __future__ import annotations
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from videos.models import Video, WatchProgress
from videos.serializers import ProgressSerializer, VideoSerializer
from videos.utils import update_watch_progress

__all__ = [
    "VideoViewSet",
    "ProgressViewSet",
    "TrailerListView",
]

CACHE_TTL: int = getattr(settings, "CACHE_TTL", 60 * 15)  # Default caching time (15 minutes)


class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Returns the list of videos, excluding trailers, with category preloaded."""
        if self.action == "list":
            return Video.objects.filter(is_trailer=False).select_related("category")
        return Video.objects.all().select_related("category")

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        """Returns the watch progress of the authenticated user."""
        return WatchProgress.objects.filter(user=self.request.user).select_related("video")

    def create(self, request, *args, **kwargs):
        """Create or update the watch progress for the video."""
        obj = update_watch_progress(
            user=request.user,
            video_id=request.data.get("video"),
            position=request.data.get("position", 0),
            duration=request.data.get("duration", 0),
        )
        return Response(
            self.get_serializer(obj).data,
            status=status.HTTP_201_CREATED
        )


@method_decorator(cache_page(CACHE_TTL * 2), name="get")  # Longer cache time for trailers
class TrailerListView(ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]  # Or IsAuthenticated based on the requirement
    
    def get_queryset(self):
        """Returns the latest 10 trailers with a maximum duration of 240 seconds."""
        return Video.objects.filter(
            is_trailer=True, 
            duration__lte=240
        ).select_related("category").order_by("-created_at")[:10]
