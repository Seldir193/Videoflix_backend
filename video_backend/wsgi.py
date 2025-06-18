import os
from pathlib import Path

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "video_backend.settings")

BASE_DIR = Path(__file__).resolve().parent.parent

django_app = get_wsgi_application()

application = WhiteNoise(
    django_app,
    root=str(BASE_DIR / "staticfiles"),
    autorefresh=getattr(settings, "WHITENOISE_AUTOREFRESH", False),
)

application.add_files(
    str(BASE_DIR / "media"),
    prefix="media/",
)
