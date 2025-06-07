from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, HttpResponse
from django.utils.http import urlsafe_base64_decode

def activate(request, uidb64: str, token: str):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])
        return redirect("http://localhost:4200/auth/login?activated=yes")
    return HttpResponse("Activation link is invalid or expired.", status=400)