# videos/apps.py
from django.apps import AppConfig


class VideosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "videos"

    def ready(self):                 # ← vier Leerzeichen weiter innen
        from . import signals        # Registriert post_save / post_delete
