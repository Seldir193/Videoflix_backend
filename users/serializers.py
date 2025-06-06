# users/serializers.py
from djoser.serializers import UserCreateSerializer as BaseCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from users.models import CustomUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from django.conf import settings



class UserCreateSerializer(BaseCreateSerializer):
    class Meta(BaseCreateSerializer.Meta):
        model = CustomUser
        fields = ("id", "email","first_name", "password", "re_password")
        extra_kwargs = {
            "first_name": {"required": False, "allow_blank": True},
            're_password': {'write_only': True},
        }

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError(
                "E-Mail-Adresse ist zu lang. Die maximale Länge ist 254 Zeichen.")
        return value

    def validate(self, data):
        if data["password"] != data["re_password"]:
            raise serializers.ValidationError({
                "re_password": ("Die Passwörter stimmen nicht überein.")
            })
        return data

    def create(self, validated_data):

        validated_data.pop('re_password', None)

        if not validated_data.get("first_name"):
            validated_data["first_name"] = validated_data["email"].split("@")[0]

        user = super().create(validated_data)
        
        user.is_active = False
        #user.save(update_fields=["first_name", "is_active"])
        user.save(update_fields=["is_active"])

        return user
    
    

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ("id", "email")











