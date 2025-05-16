"""videos/admin.py – übersichtliches Django-Admin für *Video*"""
from __future__ import annotations

from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TranslationAdmin

from .models import Video

# ---------------------------------------------------------------------------
# Import/Export-Ressource  (alle Felder, keine Excludes)
# ---------------------------------------------------------------------------

class VideoResource(resources.ModelResource):
    class Meta:
        model   = Video
        exclude = ()

# ---------------------------------------------------------------------------
# Admin-Konfiguration
# ---------------------------------------------------------------------------

@admin.register(Video)
class VideoAdmin(TranslationAdmin, ImportExportModelAdmin):
    """Admin-UI mit Thumbnail-Vorschau & Renditions-Status."""

    resource_class = VideoResource

    # -------- Listenansicht ---------------------------------------------
    list_display   = (
        "id", "thumb_tag", "title", "category", "genre", "release", "created_at", "variants_ready",
    )
    list_filter    = ("category", "genre")
    search_fields  = ("title", "description")
    date_hierarchy = "created_at"
    ordering       = ("-created_at",)

    # -------- Formular ---------------------------------------------------
    readonly_fields = ("source_variants", "thumb_tag")

    fieldsets = (
        (None, {"fields": ("title", "description", "category", "thumb_tag")}),
        ("Meta", {"fields": ("genre", "release", "director", "license_type", "license_url")}),
        ("Dateien & Pfade", {
            "description": (
                "Original hochladen – FFmpeg-Worker erzeugt anschließend automatisch "
                "alle MP4-Renditionen + Thumbnails."
            ),
            "fields": ("video_file", "source_url", "source_variants", "thumb"),
        }),
    )

    # -------- Helper -----------------------------------------------------
    @admin.display(boolean=True, description="MP4-Variants")
    def variants_ready(self, obj: Video) -> bool:  # noqa: D401
        return obj.variants_ready  # property aus Model

    @admin.display(description="Thumbnail")
    def thumb_tag(self, obj: Video) -> str:  # noqa: D401
        if obj.thumb:
            return format_html('<img src="{}" style="height:48px;border-radius:4px">', obj.thumb.url)
        return "—"