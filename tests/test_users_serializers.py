import pytest
from users.serializers import UserCreateSerializer
from users.models import CustomUser


@pytest.mark.django_db
def test_password_mismatch_validation():
    data = {
        "email": "a@example.com",
        "password": "pass1234",
        "re_password": "other",
    }
    serializer = UserCreateSerializer(data=data)
    assert serializer.is_valid() is False
    assert "re_password" in serializer.errors


@pytest.mark.django_db
def test_email_length_validation():
    long_email = f'{"x" * 250}@x.com'
    data = {
        "email": long_email,
        "password": "pass1234",
        "re_password": "pass1234",
    }
    serializer = UserCreateSerializer(data=data)
    assert serializer.is_valid() is False
    assert "email" in serializer.errors


@pytest.mark.django_db
def test_create_sets_defaults():
    data = {
        "email": "foo@example.com",
        "password": "secret123",
        "re_password": "secret123",
    }
    serializer = UserCreateSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    user = serializer.save()
    user.refresh_from_db()

    assert user.first_name == "foo"
    assert user.is_active is False
    assert CustomUser.objects.filter(email="foo@example.com").exists()
