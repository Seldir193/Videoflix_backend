from djoser.serializers import (
    UserCreateSerializer as BaseCreateSerializer,
    UserSerializer as BaseUserSerializer,
)
from rest_framework import serializers

from users.models import CustomUser
from users.utils import (
    validate_email_length,
    ensure_passwords_match,
    default_first_name_from_email,
)


class UserCreateSerializer(BaseCreateSerializer):
    re_password = serializers.CharField(write_only=True)

    class Meta(BaseCreateSerializer.Meta):
        model = CustomUser
        fields = ("id", "email", "first_name", "password", "re_password")
        extra_kwargs = {
            "first_name": {"required": False, "allow_blank": True},
            "re_password": {"write_only": True},
        }

    def validate_email(self, value):
        return validate_email_length(value)

    def validate(self, data):
        ensure_passwords_match(data["password"], data["re_password"])
        return data

    def create(self, validated_data):
        validated_data.pop("re_password", None)

        if not validated_data.get("first_name"):
            validated_data["first_name"] = default_first_name_from_email(
                validated_data["email"]
            )

        user = super().create(validated_data)
        user.is_active = False
        user.save(update_fields=["is_active"])
        return user


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ("id", "email")








