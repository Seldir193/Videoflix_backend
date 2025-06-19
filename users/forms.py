"""User creation form for the custom user model."""

from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Form for creating :class:`CustomUser` instances in the admin."""

    class Meta:
        model = CustomUser
        fields = "__all__"
