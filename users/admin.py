# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserCreationForm
from .utils import send_activation_email


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    ordering = ("email",)
    list_display = ("email", "is_staff", "is_active")
    list_display_links = ("email",)
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("email", "phone")

    @admin.action(description="Aktivierungs-Mail erneut senden")
    def send_activation(self, request, queryset):
        for user in queryset.filter(is_active=False):
            send_activation_email(user)

    actions = [send_activation]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Profil", {"fields": ("phone", "adress", "custom")}),
        (
            "Rechte",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Wichtige Daten", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
