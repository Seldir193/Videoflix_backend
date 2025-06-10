import pytest
from pathlib import Path
from django.conf import settings

from videos.signals import enqueue_pipeline, cleanup_files
from videos.tasks import create_variants


class DummyFile:
    def __init__(self, path):
        self.path = path


class DummyVideo:
    def __init__(self, id, video_file=None, source_url=None, source_variants=None):
        self.id = id
        self.video_file = video_file
        self.source_url = source_url
        self.source_variants = source_variants


def test_enqueue_pipeline_calls_enqueue(monkeypatch):
    called = {}

    def fake_enqueue(func, vid, job_timeout):
        called["args"] = (func, vid, job_timeout)

    monkeypatch.setattr("videos.signals.enqueue", fake_enqueue)

    video = DummyVideo(id=42, video_file=DummyFile("dummy"))
    enqueue_pipeline(sender=None, instance=video, created=True)
    assert called["args"] == (create_variants, 42, 7200)


def test_enqueue_pipeline_no_enqueue_when_not_created_or_no_file(monkeypatch):
    called = {"count": 0}

    def fake_enqueue(*args, **kwargs):
        called["count"] += 1

    monkeypatch.setattr("videos.signals.enqueue", fake_enqueue)

    # Not created
    v1 = DummyVideo(id=1, video_file=DummyFile("x"))
    enqueue_pipeline(None, v1, created=False)

    # No file
    v2 = DummyVideo(id=2, video_file=None)
    enqueue_pipeline(None, v2, created=True)

    assert called["count"] == 0


def test_cleanup_files_removes_all(tmp_path, monkeypatch):
    # Arrange: override MEDIA_ROOT
    monkeypatch.setattr(settings, "MEDIA_ROOT", str(tmp_path))

    # Create dummy file paths
    base = tmp_path
    orig = base / "videos" / "5" / "orig.mp4"
    variant = base / "videos" / "5" / "variant.mp4"
    thumb_img = base / "videos" / "5" / "720.mp4"
    thumb_dir = base / "thumbs" / "5"
    hero_dir = base / "hero" / "5"

    for p in (orig, variant, thumb_img):
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x")

    thumb_dir.mkdir(parents=True, exist_ok=True)
    hero_dir.mkdir(parents=True, exist_ok=True)

    video = DummyVideo(
        id=5,
        video_file=DummyFile(str(orig)),
        source_url="videos/5/variant.mp4",
        source_variants=[{"path": "videos/5/720.mp4", "height": 720}],
    )

    # Act
    cleanup_files(sender=None, instance=video)

    # Assert files removed
    assert not orig.exists()
    assert not variant.exists()
    assert not thumb_img.exists()

    # Assert directories removed
    assert not thumb_dir.exists()
    assert not hero_dir.exists()
