from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # Fields displayed in the admin list view
    list_display = ('email', 'is_staff', 'is_superuser', 'id')
    list_filter = ('is_staff', 'is_superuser')

    # Fields used in the admin detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # Fields displayed in the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)

# Register the User model with the custom admin
admin.site.register(User, UserAdmin)
