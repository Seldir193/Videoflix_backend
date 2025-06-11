from .models import WatchProgress

def update_watch_progress(user, video_id, position, duration):
    progress, _ = WatchProgress.objects.update_or_create(
        user=user,
        video_id=video_id,
        defaults={"position": position, "duration": duration}
    )
    return progress
