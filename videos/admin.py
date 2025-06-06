from __future__ import annotations
from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TranslationAdmin
from .models import Video


class VideoResource(resources.ModelResource):
    class Meta:
        model = Video
        exclude = ()


    

@admin.register(Video)
class VideoAdmin(TranslationAdmin, ImportExportModelAdmin):

    resource_class = VideoResource
    list_display = (
        "id", "thumb_tag", "title", "category","is_trailer",        
        "duration", "genre", "release", "created_at", "variants_ready",
    )
    list_filter = ("category", "genre", "is_trailer")
    search_fields = ("title", "description")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = ("source_variants", "thumb_tag" ,"duration")

    fieldsets = (
        (None, {"fields": ("title", "description", "category", "is_trailer","thumb_tag")}),
        ("Meta", {"fields": ("genre", "release",
         "director", "license_type", "license_url")}),
        ("Dateien & Pfade", {
            "description": (
                "Original hochladen – FFmpeg-Worker erzeugt anschließend automatisch "
                "alle MP4-Renditionen + Thumbnails."
            ),
            "fields": ("video_file", "source_url", "source_variants", "thumb"),
        }),
    )

    @admin.display(boolean=True, description="MP4-Variants")
    def variants_ready(self, obj: Video) -> bool:
        return obj.variants_ready

    @admin.display(description="Thumbnail")
    def thumb_tag(self, obj: Video) -> str:
        if obj.thumb:
            return format_html('<img src="{}" style="height:48px;border-radius:4px">', obj.thumb.url)
        return "—"




