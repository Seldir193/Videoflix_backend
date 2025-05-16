



"""videos/signals.py – Async-Pipeline & File‑Cleanup
------------------------------------------------------
» Beim **ersten** Upload wird sofort ein RQ‑Job enqueued, um
  • MP4‑Renditionen (1080/720/360/240) zu erzeugen und
  • Thumbnails (1280 & 320 px) abzuleiten.

» Beim Löschen eines Video‑Datensatzes werden **sämtliche** zugehörigen
  Dateien – Original, Renditionen, Thumbs – rekursiv entfernt.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch          import receiver
from django_rq                import enqueue

from .models import Video
from .tasks  import create_variants

# ---------------------------------------------------------------------------
# 1️⃣  Erstupload → FFmpeg‑Pipeline starten (django‑rq)
# ---------------------------------------------------------------------------

@receiver(post_save, sender=Video)
def enqueue_pipeline(sender, instance: Video, created: bool, **_: object) -> None:  # noqa: D401
    """Starte Transcoding nur **einmal**, direkt nach dem Erst‑Upload."""

    if created and instance.video_file:  # externes URL‑Only‑Video ignorieren
        # 2‑Stunden‑Timeout, falls große Dateien reencoded werden
        enqueue(create_variants, instance.id, job_timeout=7200)

# ---------------------------------------------------------------------------
# 2️⃣  Aufräumen: alle Dateien löschen, wenn das Video entfernt wird
# ---------------------------------------------------------------------------

@receiver(post_delete, sender=Video)
def cleanup_files(sender, instance: Video, **_: object) -> None:  # noqa: D401
    media_root = Path(settings.MEDIA_ROOT)

    # Originalupload -------------------------------------------------------
    if instance.video_file and instance.video_file.path:
        Path(instance.video_file.path).unlink(missing_ok=True)

    # MP4‑Renditionen ------------------------------------------------------
    paths: list[str] = []
    if instance.source_url:
        paths.append(instance.source_url)
    if instance.source_variants:
        paths.extend(v["path"] for v in instance.source_variants if "path" in v)

    for rel in paths:
        (media_root / rel).unlink(missing_ok=True)

    # Thumbnails & Hero Frame ---------------------------------------------
    thumb_dir = media_root / "thumbs" / str(instance.id)
    hero_dir  = media_root / "hero"   / str(instance.id)
    shutil.rmtree(thumb_dir, ignore_errors=True)
    shutil.rmtree(hero_dir,  ignore_errors=True)

