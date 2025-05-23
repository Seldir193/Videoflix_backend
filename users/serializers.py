
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
        fields = ("id", "email", "password", "re_password")
        extra_kwargs = {
            're_password': {'write_only': True},
        }
        
    def validate_email(self, value):
        """Optional: Sicherstellen, dass die E-Mail-Adresse nicht länger als 254 Zeichen ist."""
        if len(value) > 254:
            raise serializers.ValidationError("E-Mail-Adresse ist zu lang. Die maximale Länge ist 254 Zeichen.")
        return value
        
    def validate(self, data):
        """Stelle sicher, dass das Passwort und das Wiederholungspasswort übereinstimmen."""
        if data["password"] != data["re_password"]:
            raise serializers.ValidationError({
                "re_password": ("Die Passwörter stimmen nicht überein.")
            })
        return data
   

    def create(self, validated_data):
        # Entferne 're_password' aus den validierten Daten, da wir es nicht speichern
        validated_data.pop('re_password', None)

        # Benutzer erstellen
        user = super().create(validated_data)  # legt User an
        user.is_active = False  # Konto deaktivieren
        user.save(update_fields=["is_active"])
        
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(bytes(user.pk, 'utf-8'))  # bytes() statt force_bytes
        
       # domain = get_current_site(self.context["request"]).domain
        
        domain = getattr(settings, "DOMAIN", "localhost") 
        
        protocol = "https" if self.context["request"].is_secure() else "http"
        activation_link = f'{protocol}://{domain}/auth/activate/{uid}/{token}/'
       # activation_link = f'http://{domain}/auth/activate/{uid}/{token}/'

        subject = "Activate your account"
        message = render_to_string("users/email/activation_email.html", {
            "user": user,
            "activation_link": activation_link,
            "protocol": protocol,
            "domain": domain,
            "uid": uid,
            "token": token,
        })
        send_mail(subject, message, "no-reply@yourdomain.com", [user.email])

        return user

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ("id", "email")
