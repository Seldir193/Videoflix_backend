# videos/apps.py

from django.apps import AppConfig


class VideosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "videos"

    def ready(self) -> None:
        from . import translation
        from . import signals

        super().ready()
