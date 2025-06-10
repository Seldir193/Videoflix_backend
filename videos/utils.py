from .models import WatchProgress


def update_watch_progress(user, video_id, position=0, duration=0):
    obj, _ = WatchProgress.objects.update_or_create(
        user=user,
        video_id=video_id,
        defaults={"position": position, "duration": duration},
    )
    return obj
