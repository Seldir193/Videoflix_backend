
# videos/apps.py
from django.apps import AppConfig


class VideosConfig(AppConfig):
    """App-Konfiguration für das Videos-Modul."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "videos"

    def ready(self) -> None:
        """
        Wird von Django beim Start einmal aufgerufen.
        Registriert Übersetzungs­klassen und Signals.
        """
        from . import translation
        from . import signals

        super().ready()
