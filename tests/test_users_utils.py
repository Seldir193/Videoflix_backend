import pytest
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

from users.models import CustomUser
from users.utils import (
    validate_email_length,
    ensure_passwords_match,
    default_first_name_from_email,
    send_activation_email,
    get_user_from_uidb64,
    activate_user_if_valid,
)


# ─────────────────────────────── Field Validators ───────────────────────────────

def test_validate_email_length_ok():
    assert validate_email_length("a@b.de") == "a@b.de"


def test_validate_email_length_too_long():
    long_mail = f'{"x" * 250}@x.com'  # 256 > 254
    with pytest.raises(Exception):
        validate_email_length(long_mail)


def test_ensure_passwords_match_ok():
    ensure_passwords_match("abc", "abc")  # No exception should be raised


def test_ensure_passwords_match_fail():
    with pytest.raises(Exception):
        ensure_passwords_match("abc", "def")


def test_default_first_name_from_email():
    assert default_first_name_from_email("foo@bar.com") == "foo"


# ─────────────────────────────── Mail Helpers ───────────────────────────────────

@pytest.mark.django_db
def test_send_activation_email_only_if_inactive(monkeypatch):
    u = CustomUser.objects.create(email="x@example.com", is_active=False)
    called = []

    def fake_send(*_, **__):
        called.append(1)

    monkeypatch.setattr("users.utils.ActivationEmail.send", fake_send)

    send_activation_email(u)  # Should send
    send_activation_email(u)  # Still inactive, should send again

    u.is_active = True
    send_activation_email(u)  # Should NOT send as user is now active

    assert called.count(1) == 2


# ───────────────────── UID / Token-based Activation ────────────────────────

@pytest.mark.django_db
def test_get_user_from_uidb64_and_activation():
    user = CustomUser.objects.create(email="y@example.com", is_active=False)
    uidb64 = urlsafe_base64_encode(str(user.pk).encode())
    
    assert get_user_from_uidb64(uidb64) == user
    assert get_user_from_uidb64("invalid") is None

    # Valid token
    token = default_token_generator.make_token(user)
    assert activate_user_if_valid(user, token) is True
    user.refresh_from_db()
    assert user.is_active is True

    # Invalid token
    bad_token = "abc-wrong"
    assert activate_user_if_valid(user, bad_token) is False
