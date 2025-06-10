import pytest
from pathlib import Path
from django.core.exceptions import ValidationError

from videos.models import (
    video_upload_to,
    thumb_upload_to,
    hero_upload_to,
    Video,
    WatchProgress,
)
from users.models import CustomUser


@pytest.mark.django_db
def test_video_str_and_upload_paths(tmp_path):
    # Unsaved instance: id is None → "tmp"
    v = Video(title="Test Video")
    assert str(v) == "Test Video"
    assert video_upload_to(v, "file.mp4").startswith("videos/tmp/")
    assert thumb_upload_to(v, "img.png").startswith("thumbs/tmp/")
    assert hero_upload_to(v, "hero.jpg").startswith("thumbs/tmp/")

    # After saving, id is available
    v.save()
    pid = str(v.id)
    assert video_upload_to(v, "file.mp4") == f"videos/{pid}/file.mp4"


@pytest.mark.django_db
def test_clean_requires_url_or_file():
    v = Video(title="NoSource")
    with pytest.raises(ValidationError):
        v.clean()

    # URL present → clean passes
    v.url = "http://example.com/video.mp4"
    v.clean()

    # video_file present → clean passes
    v.url = ""
    v.video_file = "dummy.mp4"  # FileField accepts a path-like object
    v.clean()


def make_variants_list(heights):
    return [{"path": f"p{h}.mp4", "height": h} for h in heights]


def test_variants_ready_and_get_variant():
    v = Video(title="Variants")
    
    # No variants → False, get_variant None
    assert v.variants_ready is False
    assert v.get_variant(360) is None

    # Partial variants → False
    v.source_variants = make_variants_list([360])
    assert v.variants_ready is False
    assert v.get_variant(360) == "p360.mp4"
    assert v.get_variant(720) is None

    # Full variants → True
    v.source_variants = make_variants_list([360, 720])
    assert v.variants_ready is True
    # Ordering independent
    assert set(v.get_variant(h) for h in (360, 720)) == {"p360.mp4", "p720.mp4"}


@pytest.mark.django_db
def test_watchprogress_str_and_unique():
    user = CustomUser.objects.create_user(email="u@x.de", password="pw")
    video = Video.objects.create(title="VP")
    
    # First progress
    wp1 = WatchProgress.objects.create(user=user, video=video, position=10, duration=100)
    assert str(wp1).startswith("u@x.de @") and "→ 10.0s" in str(wp1)

    # Update existing via create raises IntegrityError if duplicate
    with pytest.raises(Exception):
        WatchProgress.objects.create(user=user, video=video)
