from __future__ import annotations

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from .models import Video, WatchProgress
from .serializers import ProgressSerializer, VideoSerializer
from videos.utils import update_watch_progress
from rest_framework.decorators import action


__all__ = [
    "VideoViewSet",
    "ProgressViewSet",
]

CACHE_TTL: int = getattr(settings, "CACHE_TTL", 60 * 15)


@method_decorator(cache_page(CACHE_TTL), name="list")
@method_decorator(cache_page(CACHE_TTL), name="retrieve")
class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        if self.action == "list":
            return Video.objects.filter(is_trailer=False)
        return Video.objects.all()

class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WatchProgress.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=["get"])
    def get_progress(self, request, *args, **kwargs):
        video_id = request.query_params.get("video")
        progress = WatchProgress.objects.filter(user=request.user, video_id=video_id).first()
        
        if progress:
            return Response({"position": progress.position, "duration": progress.duration}, status=200)
        
        return Response({"position": 0, "duration": 0}, status=200)


    def create(self, request, *args, **kwargs):
        obj = update_watch_progress(
            user=request.user,
            video_id=request.data.get("video"),
            position=request.data.get("position", 0),
            duration=request.data.get("duration", 0),
        )
        return Response(self.get_serializer(obj).data, status=status.HTTP_201_CREATED)

    http_method_names = ["get", "post", "head", "options"]


class TrailerList(ListAPIView):
    serializer_class = VideoSerializer
    queryset = Video.objects.filter(is_trailer=True, duration__lte=240)
    permission_classes = [IsAuthenticated]






