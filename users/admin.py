from django.contrib import admin
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    fieldsets = (

        (
            'Indivuduelle Date',
            {
                'fields': (
                    'custom',
                    'phone',
                    'adress',
                )
            }
        ),
         *UserAdmin.fieldsets,
            
        
        
    )