# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm
from djoser.email import ActivationEmail


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    ordering = ("email",)
    list_display = ("email", "is_staff", "is_active")
    list_display_links = ("email",)
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("email", "phone")

    # ---- Aktionen ---------------------------------------------------
    @admin.action(description="Aktivierungs-Mail erneut senden")
    def send_activation(self, request, queryset):
        for user in queryset:
            if not user.is_active:
                context = {'user': user}
                ActivationEmail(context).send(to=[user.email])
    actions = [send_activation]
    # ---- Detailansicht ----------------------------------------------
    fieldsets = (
        (None,      {"fields": ("email", "password")}),
        ("Profil",  {"fields": ("phone", "adress", "custom")}),
        ("Rechte",  {"fields": ("is_active", "is_staff", "is_superuser",
                                "groups", "user_permissions")}),
        ("Wichtige Daten", {"fields": ("last_login", "date_joined")}),
    )

    # ---- Benutzer hinzufügen ----------------------------------------
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2",
                       "is_staff", "is_active"),
        }),
    )
