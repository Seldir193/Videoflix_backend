from django.shortcuts import redirect, HttpResponse

from users.utils import get_user_from_uidb64, activate_user_if_valid


def activate(request, uidb64: str, token: str):
    user = get_user_from_uidb64(uidb64)

    if activate_user_if_valid(user, token):
        return redirect("http://localhost:4200/auth/login?activated=yes")

    return HttpResponse("Activation link is invalid or expired.", status=400)
