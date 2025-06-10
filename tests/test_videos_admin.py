import pytest
from django.contrib.admin.sites import AdminSite
from django.utils.html import format_html

from videos.admin import VideoAdmin
from videos.models import Video


@pytest.fixture
def admin_site():
    return AdminSite()


@pytest.fixture
def video_admin(admin_site):
    return VideoAdmin(Video, admin_site)


def test_variants_ready_property_true(video_admin):
    vid = Video()
    vid.source_variants = [{"path": "p1", "height": 360}, {"path": "p2", "height": 720}]
    assert video_admin.variants_ready(vid) is True


def test_variants_ready_property_false(video_admin):
    vid = Video()
    vid.source_variants = [{"path": "p1", "height": 360}]
    assert video_admin.variants_ready(vid) is False


def test_thumb_tag_no_thumb(video_admin):
    vid = Video()
    vid.thumb = None
    assert video_admin.thumb_tag(vid) == "—"


def test_thumb_tag_with_thumb(video_admin):
    class DummyImage:
        url = "/media/tn.png"

    vid = Video()
    vid.thumb = DummyImage()
    expected = format_html(
        '<img src="{}" style="height:48px;border-radius:4px">', vid.thumb.url
    )
    assert video_admin.thumb_tag(vid) == expected
