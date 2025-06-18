from djoser.email import ActivationEmail, PasswordResetEmail
from django.conf import settings
from django.templatetags.static import static
import base64
from pathlib import Path


def add_logo_context(request, ctx):
    """Ergänzt ctx um logo_data_uri ODER logo_url + protocol/domain."""
    ctx["protocol"] = settings.FRONTEND_PROTOCOL
    ctx["domain"] = settings.FRONTEND_DOMAIN

    if settings.DEBUG:
        logo_path = Path(settings.BASE_DIR, "static", "img", "logo_vf.png")
        try:
            with open(logo_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            ctx["logo_data_uri"] = f"data:image/png;base64,{b64}"
        except FileNotFoundError:
            ctx["logo_data_uri"] = ""
    else:
        ctx["logo_url"] = request.build_absolute_uri(static("img/logo_vf.png"))


class CustomActivationEmail(ActivationEmail):
    template_name = "djoser/email/activation.html"
    plain_template_name = "djoser/email/activation.txt"
    subject = "Aktiviere dein Konto bei Videoflix"

    def get_context_data(self):
        ctx = super().get_context_data()
        add_logo_context(self.request, ctx)
        return ctx


class CustomPasswordResetEmail(PasswordResetEmail):
    template_name = "djoser/email/password_reset.html"
    plain_template_name = "djoser/email/password_reset.txt"
    subject = "Setze dein Videoflix-Passwort zurück"

    def get_context_data(self):
        ctx = super().get_context_data()
        add_logo_context(self.request, ctx)
        return ctx
