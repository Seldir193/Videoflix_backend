from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, URLValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = [
    "Video",
    "WatchProgress",
]


def video_upload_to(instance: Video, filename: str) -> str:
    return f"videos/{instance.id or 'tmp'}/{filename}"


def thumb_upload_to(instance: Video, filename: str) -> str:
    return f"thumbs/{instance.id or 'tmp'}/{filename}"


def hero_upload_to(instance: Video, filename: str) -> str:
    return f"thumbs/{instance.id or 'tmp'}/{filename}"


class Video(models.Model):
    class Category(models.TextChoices):
        NEW = "New on Videoflix", _("New on Videoflix")
        DOCU = "Documentary", _("Documentary")
        DRAMA = "Drama", _("Drama")
        ROM = "Romance", _("Romance")

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    duration = models.PositiveIntegerField(null=True, blank=True)
    is_trailer = models.BooleanField(default=False)

    genre = models.CharField(max_length=100, blank=True)
    release = models.DateField(null=True, blank=True)
    director = models.CharField(max_length=200, blank=True)

    license_type = models.CharField(max_length=50, blank=True)
    license_url = models.URLField(
        blank=True,
        null=True,
        validators=[URLValidator()],
    )

    category = models.CharField(
        max_length=30,
        choices=Category.choices,
        default=Category.NEW,
    )

    url = models.URLField(blank=True, null=True)
    video_file = models.FileField(
        upload_to=video_upload_to,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["mp4", "mov", "mkv", "m4v"])],
    )

    source_url = models.URLField(max_length=500, blank=True, null=True)
    source_variants = models.JSONField(blank=True, null=True)

    thumb = models.ImageField(upload_to=thumb_upload_to, blank=True, null=True)
    hero_frame = models.ImageField(upload_to=hero_upload_to, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [models.Index(fields=["created_at"])]

    def clean(self):
        super().clean()
        if not self.url and not self.video_file:
            raise ValidationError(
                _("Entweder ein Upload oder eine externe URL ist erforderlich.")
            )

    def __str__(self) -> str:
        return self.title

    @property
    def variants_ready(self) -> bool:
        if not self.source_variants:
            return False
        heights = {v["height"] for v in self.source_variants}
        return {720, 360}.issubset(heights)

    def get_variant(self, height: int) -> str | None:
        if not self.source_variants:
            return None
        for v in self.source_variants:
            if v["height"] == height:
                return v["path"]
        return None


class WatchProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    position = models.FloatField(default=0)
    duration = models.FloatField(default=0)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "video")
        ordering = ("-updated",)
        indexes = [models.Index(fields=["user", "video"])]

    def __str__(self) -> str:
        return f"{self.user} @ {self.video} → {self.position:.1f}s"
