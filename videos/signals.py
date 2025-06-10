from __future__ import annotations

import shutil
from pathlib import Path

from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_rq import enqueue

from .models import Video
from .tasks import create_variants


@receiver(post_save, sender=Video)
def enqueue_pipeline(sender, instance: Video, created: bool, **_: object) -> None:
    if created and instance.video_file:
        enqueue(create_variants, instance.id, job_timeout=7200)


@receiver(post_delete, sender=Video)
def cleanup_files(sender, instance: Video, **_: object) -> None:
    media_root = Path(settings.MEDIA_ROOT)

    if instance.video_file and instance.video_file.path:
        Path(instance.video_file.path).unlink(missing_ok=True)

    paths: list[str] = []
    if instance.source_url:
        paths.append(instance.source_url)
    if instance.source_variants:
        paths.extend(
            v["path"] for v in instance.source_variants if "path" in v
        )

    for rel in paths:
        (media_root / rel).unlink(missing_ok=True)

    thumb_dir = media_root / "thumbs" / str(instance.id)
    hero_dir = media_root / "hero" / str(instance.id)

    shutil.rmtree(thumb_dir, ignore_errors=True)
    shutil.rmtree(hero_dir, ignore_errors=True)
