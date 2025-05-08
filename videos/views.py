from django.shortcuts import render
from rest_framework import viewsets
from .models import Video
from videos.serializers import VideoSerializer

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page 
from django.conf import settings

from django.core.cache import cache
from django.utils.decorators import method_decorator


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


#@cache_page(CACHE_TTL)

@method_decorator(cache_page(CACHE_TTL), name="list")
@method_decorator(cache_page(CACHE_TTL), name="retrieve")

class VideoViewSet(viewsets.ModelViewSet):
    
    queryset = Video.objects.all().order_by("-created_at")
    serializer_class = VideoSerializer
