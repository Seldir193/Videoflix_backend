import pytest
from django.test import RequestFactory
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

from users.models import CustomUser
from users.views import activate


@pytest.mark.django_db
def test_activate_view_success():
    user = CustomUser.objects.create(email="ok@example.com", is_active=False)
    uidb64 = urlsafe_base64_encode(str(user.pk).encode())
    token = default_token_generator.make_token(user)

    req = RequestFactory().get("/")
    resp = activate(req, uidb64, token)

    assert resp.status_code == 302
    assert resp.url == "http://localhost:4200/auth/login?activated=yes"
    
    user.refresh_from_db()
    assert user.is_active is True


@pytest.mark.django_db
def test_activate_view_invalid_token():
    user = CustomUser.objects.create(email="bad@example.com", is_active=False)
    uidb64 = urlsafe_base64_encode(str(user.pk).encode())
    bad_token = "wrong-token"

    req = RequestFactory().get("/")
    resp = activate(req, uidb64, bad_token)

    assert resp.status_code == 400
    assert b"invalid or expired" in resp.content.lower()
