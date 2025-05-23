
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse

def activate(request, uidb64: str, token: str) -> HttpResponse:
    try:
        # UID dekodieren und Benutzer abrufen
        uid = str(urlsafe_base64_decode(uidb64))  # Verwende str() statt smart_text
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    # Token validieren und Benutzer aktivieren
    if user is not None and default_token_generator.check_token(user, token):  # Gibt True oder False zurück
        user.is_active = True
        user.save()
        # Erfolgreiche Aktivierung: Weiterleitung zur Login-Seite
        return redirect("auth:login")
    else:
        # Fehlerseite, wenn der Token ungültig oder abgelaufen ist
        return HttpResponse('Activation link is invalid or expired.')
