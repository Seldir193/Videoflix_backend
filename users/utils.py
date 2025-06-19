"""Utility helpers for user registration and activation."""

from djoser.email import ActivationEmail
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode


def send_activation_email(user):
    """Dispatch an activation e‑mail if the user is inactive."""
    if user.is_active:
        return

    context = {"user": user}
    ActivationEmail(context).send(to=[user.email])


def validate_email_length(email: str, max_length: int = 254) -> str:
    """Ensure *email* does not exceed *max_length* characters."""
    if len(email) > max_length:
        raise serializers.ValidationError(
            f"E-Mail-Adresse ist zu lang. Die maximale Länge ist {max_length} Zeichen."
        )
    return email


def ensure_passwords_match(password: str, repeated: str) -> None:
    """Raise when *password* and *repeated* differ."""
    if password != repeated:
        raise serializers.ValidationError(
            {"re_password": "Die Passwörter stimmen nicht überein."}
        )


def default_first_name_from_email(email: str) -> str:
    """Return the part before the @ as a default first name."""
    return email.split("@", 1)[0]


def get_user_from_uidb64(uidb64: str):
    """Decode *uidb64* and fetch the corresponding user or None."""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        return get_user_model().objects.get(pk=uid)
    except Exception:
        return None


def activate_user_if_valid(user, token: str) -> bool:
    """Activate *user* if *token* is valid; return ``True`` on success."""
    if user and default_token_generator.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])
        return True
    return False
