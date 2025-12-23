"""FFmpeg tasks: create MP4 renditions and thumbnails."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Final

from django.conf import settings
from django_rq import enqueue

from .models import Video

RENDITIONS: Final[list[tuple[str, int, str]]] = [
    ("1080p", 1080, "5000k"),
    ("720p", 720, "3000k"),
    ("360p", 360, "800k"),
    ("240p", 240, "400k"),
]

FFMPEG = settings.__dict__.get("FFMPEG_BINARY", "ffmpeg")
FFPROBE = settings.__dict__.get("FFPROBE_BINARY", "ffprobe")


def run(cmd: list[str]) -> None:
    """Execute *cmd* via ``subprocess`` and abort on non‑zero exit."""
    print("▶", " ".join(cmd))
    cp = subprocess.run(cmd, text=True, capture_output=True)

    if cp.stdout:
        print(cp.stdout)
    if cp.stderr:
        print(cp.stderr)

    cp.check_returncode()


def create_variants(video_id: int) -> None:
    """Generate H.264 MP4 renditions for the given *video_id*."""
    vid = Video.objects.get(pk=video_id)

    if not vid.video_file:
        raise FileNotFoundError("Original‑Upload fehlt – nichts zu tun.")

    src = Path(vid.video_file.path)
    out_dir = Path(settings.MEDIA_ROOT, "videos", str(video_id))
    out_dir.mkdir(parents=True, exist_ok=True)

    variants: dict[int, str] = {}

    for tag, height, br in RENDITIONS:
        dst = out_dir / f"{src.stem}_{tag}.mp4"

        if dst.exists():
            variants[height] = dst.relative_to(settings.MEDIA_ROOT).as_posix()
            continue

        run([
            FFMPEG, "-y", "-i", str(src),
            "-vf", f"scale=-2:{height}",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k", "-ac", "2",
            "-movflags", "+faststart",
            str(dst),
        ])
        variants[height] = dst.relative_to(settings.MEDIA_ROOT).as_posix()

    if not variants:
        raise RuntimeError("Keine Renditionen erzeugt – FFmpeg fehlgeschlagen?")

    preferred = 720 if 720 in variants else max(variants)
    vid.source_url = variants[preferred]
    vid.source_variants = [
        {"path": variants[h], "height": h} for h in sorted(variants, reverse=True)
    ]
    vid.save(update_fields=["source_url", "source_variants"])

    #enqueue(extract_thumb, video_id, str(src))
    preferred_abs = Path(settings.MEDIA_ROOT, variants[preferred])
    enqueue(extract_thumb, video_id, str(preferred_abs))



def extract_thumb(video_id: int, src_path: str) -> None:
    """Grab 1280 px hero‐frame + 320 px thumbnail and set duration."""
    vid = Video.objects.get(pk=video_id)

    hero_dir = Path(settings.MEDIA_ROOT, "hero", str(video_id))
    thumb_dir = Path(settings.MEDIA_ROOT, "thumbs", str(video_id))
    hero_dir.mkdir(parents=True, exist_ok=True)
    thumb_dir.mkdir(parents=True, exist_ok=True)

    hero = hero_dir / "hero.jpg"
    thumb = thumb_dir / "thumb.png"

    dur = float(subprocess.check_output([
        FFPROBE, "-v", "error", "-select_streams", "v:0",
        "-show_entries", "format=duration",
        "-of", "default=nokey=1:noprint_wrappers=1",
        src_path,
    ]))
    #ts = max(dur * 0.25, 1)
    ts = min(max(10.0, 1.0), max(dur - 1.0, 1.0))

    if not hero.exists():
        run([
          #  FFMPEG, "-y", "-ss", str(ts), "-i", src_path,
            FFMPEG, "-y", "-i", src_path, "-ss", str(ts),

            "-vframes", "1", "-vf", "scale=1280:-1",
            str(hero),
        ])

    if not thumb.exists():
        run([
           # FFMPEG, "-y", "-ss", str(ts), "-i", src_path,
            FFMPEG, "-y", "-i", src_path, "-ss", str(ts),

            "-vframes", "1", "-vf", "scale=320:-1",
            str(thumb),
        ])

    vid.hero_frame = hero.relative_to(settings.MEDIA_ROOT).as_posix()
    vid.thumb = thumb.relative_to(settings.MEDIA_ROOT).as_posix()

    if not vid.duration:
        vid.duration = round(dur)

    vid.save(update_fields=["hero_frame", "thumb", "duration"])

    print("Variants:", json.dumps(vid.source_variants, indent=2))
