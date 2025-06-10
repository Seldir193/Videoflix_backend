import pytest
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory

from users.models import CustomUser
from users.admin import CustomUserAdmin


@pytest.mark.django_db
def test_send_activation_filters_inactive_users(monkeypatch):
    site = AdminSite()
    admin = CustomUserAdmin(CustomUser, site)
    rf = RequestFactory()
    request = rf.get("/admin/users/customuser/")

    inactive_user = CustomUser.objects.create(email="a@example.com", is_active=False)
    active_user = CustomUser.objects.create(email="b@example.com", is_active=True)

    called = []

    def fake_send(u):
        called.append(u.pk)

    monkeypatch.setattr("users.admin.send_activation_email", fake_send)

    qs = CustomUser.objects.filter(pk__in=[inactive_user.pk, active_user.pk])
    admin.send_activation(request, qs)

    # Assert that only the inactive user has been called for sending the activation email
    assert called == [inactive_user.pk]
