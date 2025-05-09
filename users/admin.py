
    
    
# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models  import CustomUser
from .forms   import CustomUserCreationForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin-Ansicht für das E-Mail-basierte CustomUser-Modell (ohne username)."""

    add_form = CustomUserCreationForm              # eigenes createsuperuser-Formular
    ordering  = ("email",)
    list_display  = ("email", "is_staff", "is_active")
    search_fields = ("email",)

    # ─────────────────────────── Felder in der Detail-Ansicht ───────────────────────────
    fieldsets = (
        (None, {"fields": ("email", "password")}),             # Basis
        ("Profil",  {"fields": ("phone", "adress", "custom")}),# deine Extrafelder
        ("Rechte",  {"fields": ("is_active", "is_staff", "is_superuser",
                                "groups", "user_permissions")}),
        ("Wichtige Daten", {"fields": ("last_login", "date_joined")}),
    )

    # Felder im „Benutzer hinzufügen“-Dialog
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2",
                       "is_staff", "is_active"),
        }),
    )



