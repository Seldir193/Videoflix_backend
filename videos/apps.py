"""App configuration for the *videos* Django app."""

from django.apps import AppConfig


class VideosConfig(AppConfig):
    """AppConfig for the Videos application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "videos"

    def ready(self) -> None:  # noqa: D401
        """Import translations and signal handlers."""
        from . import translation  # noqa: WPS433, F401
        from . import signals  # noqa: WPS433, F401

        super().ready()
