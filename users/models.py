"""Custom user model with e‑mail as the primary identifier."""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """Manager for :class:`CustomUser`. Uses e‑mail for authentication."""

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """Create an inactive user with the given e‑mail and password."""
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", False)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create an active staff superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Videoflix user model. Username is kept for legacy; e‑mail is unique."""

    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
    )
    phone = models.CharField(
        max_length=15,
        default="",
        blank=True,
    )
    adress = models.CharField(  # note: typo preserved for compatibility
        max_length=150,
        default="",
        blank=True,
    )
    custom = models.CharField(
        max_length=1000,
        default="",
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
