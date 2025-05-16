"""videos/serializers.py – clean & type‑safe DRF serializers"""
from __future__ import annotations

from django.conf import settings
from rest_framework import serializers

from .models import Video, WatchProgress

__all__ = [
    "VideoSerializer",
    "ProgressSerializer",
]


class VideoSerializer(serializers.ModelSerializer):
    """Vollständige Repräsentation eines *Video*‑Datensatzes + Convenience‑Felder."""

    video_file_url = serializers.SerializerMethodField()
    sources        = serializers.SerializerMethodField()

    class Meta:
        model  = Video
        fields = "__all__"  # → liefert auch video_file_url & sources
        read_only_fields = (
            "source_url",
            "source_variants",
            "thumb",
            "hero_frame",
        )
        extra_kwargs = {
            "video_file": {"required": False, "allow_null": True},
            "url"       : {"required": False, "allow_blank": True},
        }

    # ------------------------------------------------------------------
    # Convenience: primäre MP4‑Quelle (720p oder Original)
    # ------------------------------------------------------------------
    def get_video_file_url(self, obj: Video) -> str | None:  # noqa: D401
        request = self.context.get("request")
        if not request:
            return None

        # bevorzugte Rendition (720p) …
        if obj.source_url:
            return request.build_absolute_uri(settings.MEDIA_URL + obj.source_url)

        # … andernfalls das Original
        if obj.video_file:
            return request.build_absolute_uri(obj.video_file.url)

        return None

    # ------------------------------------------------------------------
    # Plyr‑Quellenliste (höchste Auflösung zuerst)
    # ------------------------------------------------------------------
    def get_sources(self, obj: Video) -> list[dict[str, int | str]]:  # noqa: D401
        request = self.context.get("request")
        if not (request and obj.source_variants):
            return []

        ordered = sorted(obj.source_variants, key=lambda v: v["height"], reverse=True)

        return [
            {
                "src" : request.build_absolute_uri(settings.MEDIA_URL + v["path"]),
                "type": "video/mp4",
                "size": v["height"],
            }
            for v in ordered
        ]

    # ------------------------------------------------------------------
    # Validierung: Mindestens eine Quelle (URL oder Upload) erforderlich
    # ------------------------------------------------------------------
    def validate(self, data: dict) -> dict:  # noqa: D401
        if not data.get("url") and not data.get("video_file"):
            raise serializers.ValidationError(
                "Bitte entweder eine externe URL oder eine Videodatei hochladen.")
        return data


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model  = WatchProgress
        fields = ("id", "video", "position", "duration", "updated")
        read_only_fields = ("updated",)
