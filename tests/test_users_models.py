import pytest
from users.models import CustomUser


@pytest.mark.django_db
def test_create_user_defaults():
    user = CustomUser.objects.create_user(
        email="Foo@Example.COM", password="secret123"
    )
    assert user.email == "Foo@example.com"
    assert user.check_password("secret123")
    assert user.is_active is False
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_create_user_requires_email():
    with pytest.raises(ValueError):
        CustomUser.objects.create_user(email="", password="x")


@pytest.mark.django_db
def test_create_superuser_flags():
    admin = CustomUser.objects.create_superuser(
        email="admin@example.com", password="root123"
    )
    assert admin.is_staff is True
    assert admin.is_superuser is True
    assert admin.is_active is True
