from __future__ import annotations
from django.conf import settings
from rest_framework import serializers
from .models import Video, WatchProgress

__all__ = [
    "VideoSerializer",
    "ProgressSerializer",
]

class VideoSerializer(serializers.ModelSerializer):
    video_file_url = serializers.SerializerMethodField()
    sources = serializers.SerializerMethodField()

    class Meta:
        model = Video
        exclude = (
            "title_de", "title_en",
            "description_de", "description_en",
        )

        read_only_fields = (
            "source_url",
            "source_variants",
            "thumb",
            "hero_frame",
        )

        extra_kwargs = {
            "video_file": {"required": False, "allow_null": True},
            "url":        {"required": False, "allow_blank": True},
        }


    def to_representation(self, instance: Video):
        rep = super().to_representation(instance)

        request = self.context.get("request")
        lang = getattr(request, "LANGUAGE_CODE", "de") or "de"

        rep["title"] = (
            getattr(instance, f"title_{lang}", None)
            or getattr(instance, "title_de", None)
            or getattr(instance, "title_en", None)
            or instance.title
        )
        rep["description"] = (
            getattr(instance, f"description_{lang}", None)
            or getattr(instance, "description_de", None)
            or getattr(instance, "description_en", None)
            or instance.description
        ) 

        return rep


    def get_video_file_url(self, obj: Video) -> str | None:
        request = self.context.get("request")
        if not request:
            return None

        if obj.source_url:
            return request.build_absolute_uri(settings.MEDIA_URL + obj.source_url)

        if obj.video_file:
            return request.build_absolute_uri(obj.video_file.url)

        return None

    def get_sources(self, obj: Video) -> list[dict[str, int | str]]:
        request = self.context.get("request")
        if not (request and obj.source_variants):
            return []

        ordered = sorted(obj.source_variants,
                         key=lambda v: v["height"], reverse=True)

        return [
            {
                "src": request.build_absolute_uri(settings.MEDIA_URL + v["path"]),
                "type": "video/mp4",
                "size": v["height"],
            }
            for v in ordered
        ]

    def validate(self, data: dict) -> dict:
        if not data.get("url") and not data.get("video_file"):
            raise serializers.ValidationError(
                "Bitte entweder eine externe URL oder eine Videodatei hochladen.")
        return data


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchProgress
        fields = ("id", "video", "position", "duration", "updated")
        read_only_fields = ("updated",)