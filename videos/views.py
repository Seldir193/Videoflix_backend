from __future__ import annotations

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import Video, WatchProgress
from .serializers import ProgressSerializer, VideoSerializer
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status


__all__ = [
    "VideoViewSet",
    "ProgressViewSet",
]

CACHE_TTL: int = getattr(settings, "CACHE_TTL", 60 * 15)


@method_decorator(cache_page(CACHE_TTL), name="retrieve")
class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        if self.action == "list":
            return Video.objects.filter(is_trailer=False)
        return Video.objects.all()


class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class   = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names  = ["get", "post", "head", "options"]

    def get_queryset(self):
        return WatchProgress.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        video_id = request.data.get("video")
        position = request.data.get("position")
        duration = request.data.get("duration")

        progress, _ = WatchProgress.objects.update_or_create(
            user=request.user,
            video_id=video_id,
            defaults={"position": position, "duration": duration},
        )
        return Response(
            self.get_serializer(progress).data, status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, url_path="get_progress", methods=["get"])
    def get_progress(self, request):
        video_id = request.query_params.get("video")

        obj = WatchProgress.objects.filter(
            user=request.user, video_id=video_id
        ).first()                          

        if not obj:
            return Response({"position": 0, "duration": 0})

        return Response({
            "id":       obj.id,
            "position": obj.position,
            "duration": obj.duration,
        })

class TrailerList(ListAPIView):
    serializer_class = VideoSerializer
    queryset = Video.objects.filter(is_trailer=True, duration__lte=240)
    permission_classes = [IsAuthenticated]



