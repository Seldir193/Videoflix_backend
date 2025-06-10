import pytest
from types import SimpleNamespace
from django.conf import settings
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from videos.models import Video, WatchProgress
from videos.serializers import VideoSerializer, ProgressSerializer
from users.models import CustomUser


class DummyRequest:
    def __init__(self, base, lang="de"):
        self._base = base
        self.LANGUAGE_CODE = lang

    def build_absolute_uri(self, path):
        return f"{self._base}{path}"


def test_get_video_file_url_prefers_source_url():
    v = Video()
    v.source_url = "variants/720.mp4"
    v.video_file = None

    req = DummyRequest("http://testserver", "de")
    assert VideoSerializer(context={"request": req}).get_video_file_url(v) == \
        "http://testserver" + settings.MEDIA_URL + "variants/720.mp4"


def test_get_video_file_url_uses_video_file():
    v = Video()
    v.source_url = ""
    v.video_file = SimpleNamespace(url="/media/videos/foo.mp4")

    req = DummyRequest("http://testserver", "de")
    assert VideoSerializer(context={"request": req}).get_video_file_url(v) == \
        "http://testserver" + "/media/videos/foo.mp4"


def test_get_sources_empty_and_ordering():
    v = Video()
    v.source_variants = []
    req = DummyRequest("http://testserver", "de")
    assert VideoSerializer(context={"request": req}).get_sources(v) == []

    # Unordered heights
    v.source_variants = [
        {"path": "p360.mp4", "height": 360},
        {"path": "p720.mp4", "height": 720},
    ]
    sources = VideoSerializer(context={"request": req}).get_sources(v)
    assert sources[0]["size"] == 720 and sources[1]["size"] == 360
    assert all("src" in s and "type" in s for s in sources)


def test_to_representation_uses_language_fallback(monkeypatch):
    v = Video(title="Base", description="Desc")
    # Simulate translations
    v.title_de = "TitelDE"
    v.description_de = ""
    factory = APIRequestFactory()
    req = factory.get("/")
    req.LANGUAGE_CODE = "de"
    serializer = VideoSerializer(v, context={"request": req})
    rep = serializer.to_representation(v)
    assert rep["title"] == "TitelDE"
    
    # Fallback to base if no translation
    v.title_de = ""
    rep2 = serializer.to_representation(v)
    assert rep2["title"] == "Base"


def test_validate_requires_url_or_file():
    s = VideoSerializer(data={}, context={"request": DummyRequest("x")})
    with pytest.raises(serializers.ValidationError):
        s.validate({})

    # With URL
    assert VideoSerializer(context={"request": DummyRequest("x")}).validate({"url": "http://a"}) == {"url": "http://a"}

    # With file
    assert VideoSerializer(context={"request": DummyRequest("x")}).validate({"video_file": "dummy.mp4"}) == {"video_file": "dummy.mp4"}


@pytest.mark.django_db
def test_progress_serializer_and_str():
    user = CustomUser.objects.create_user(email="a@b.com", password="p")
    video = Video.objects.create(title="T")
    wp = WatchProgress.objects.create(user=user, video=video, position=5, duration=50)
    ser = ProgressSerializer(wp)
    data = ser.data
    assert data["position"] == 5
    assert data["duration"] == 50
    assert "updated" in data
