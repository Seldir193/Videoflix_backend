from __future__ import annotations
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions, status, viewsets
from rest_framework.generics import ListAPIView
from videos.models import Video, WatchProgress
from videos.serializers import VideoSerializer 

import pytest
from django.urls import reverse
from rest_framework.test import APIClient


__all__ = [
    "VideoViewSet",
    "ProgressViewSet",
    "TrailerListView",
]

CACHE_TTL: int = getattr(settings, "CACHE_TTL", 60 * 15)  # Default caching time (15 minutes)




@pytest.fixture(autouse=True)
def ensure_atomic_requests_key(settings):
    """
    Django 5.2 erwartet DATABASES['default']['ATOMIC_REQUESTS'].
    Füge ihn testweise mit False hinzu, falls er fehlt.
    """
    db = settings.DATABASES["default"]
    db.setdefault("ATOMIC_REQUESTS", False)


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






@pytest.fixture
def user(django_user_model, db):
    return django_user_model.objects.create_user(
        email="tester@example.com",
        password="secret123",
    )


@pytest.fixture
def api_client(user):
    """Authentifizierter DRF-Client."""
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def video(db):
    return Video.objects.create(title="Demo-Clip")

def test_create_progress(api_client, user, video):
    url = reverse("progress-list")                  
    payload = {"video": video.id, "position": 12, "duration": 90}

    resp = api_client.post(url, payload, format="json")

    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.json()

    wp = WatchProgress.objects.get(id=data["id"])
    assert wp.user == user
    assert wp.video == video
    assert wp.position == 12
    assert wp.duration == 90


def test_second_post_updates_same_row(api_client, video):
    url = reverse("progress-list")

    api_client.post(url, {"video": video.id, "position": 10, "duration": 80},
                    format="json")
    api_client.post(url, {"video": video.id, "position": 25, "duration": 80},
                    format="json")

    wp = WatchProgress.objects.get()
    assert wp.position == 25
    assert WatchProgress.objects.count() == 1

def test_get_progress_returns_entry(api_client, user, video):
    wp = WatchProgress.objects.create(
        user=user, video=video, position=40, duration=100
    )

    url = reverse("progress-get-progress")        
    resp = api_client.get(url, {"video": video.id})

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {
        "id": wp.id,
        "position": 40,
        "duration": 100,
    }


# --- ersetze NUR diese Funktion ---------------------------------------------

def test_get_progress_without_entry_returns_default_zero(api_client, video):
    """
    Gibt es noch keinen WatchProgress-Eintrag, muss der View
    {"position": 0, "duration": 0} mit HTTP 200 liefern.
    """
    url  = reverse("progress-get-progress")
    resp = api_client.get(url, {"video": video.id})

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"position": 0, "duration": 0}


def test_endpoints_require_auth(video):
    client = APIClient()
    url_list = reverse("progress-list")
    url_get  = reverse("progress-get-progress") + f"?video={video.id}"

    assert client.post(url_list, {}).status_code == status.HTTP_401_UNAUTHORIZED
    assert client.get(url_get).status_code  == status.HTTP_401_UNAUTHORIZED



















