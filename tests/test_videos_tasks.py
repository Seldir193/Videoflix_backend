import pytest
from videos.models import Video

@pytest.fixture
def video_file(tmp_path):
    """Fixture to create a temporary video file."""
    video_path = tmp_path / "test_video.mp4"
    video_path.write_text("dummy video content")  # Create a dummy video file
    return video_path


@pytest.fixture
def video_instance():
    """Fixture to create a Video instance for testing."""
    return Video.objects.create(
        title="Test Video",
        video_file="dummy/path",  # Provide a path for the video file
        source_url=None,  # Initialized as None to test various cases
        source_variants=None
    )
