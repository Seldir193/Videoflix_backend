
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
        # pylint: disable=import-outside-toplevel
        from . import translation  # noqa: F401  – modeltranslation registrieren
        from . import signals      # noqa: F401  – post_save / post_delete binden

        super().ready()
