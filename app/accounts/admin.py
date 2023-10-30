from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from accounts.models import User

# Register your models here.


class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "first_name",
        "is_active",
        "last_name",
        "created_at",
    )
    list_filter = ["is_active"]
    fieldsets = (
        (
            None,
            {
                "fields": [
                    "password",
                ]
            },
        ),
        ("Personal Info", {"fields": ["email", "first_name", "last_name"]}),
        (
            "Permissions",
            {
                "fields": [
                    "is_admin",
                    "is_superadmin",
                    "is_staff",
                    "is_active",
                ]
            },
        ),
        (
            "Info",
            {
                "fields": (
                    "created_at",
                    "edited_at",
                )
            },
        ),
    )
    readonly_fields = ["created_at", "edited_at"]
    filter_horizontal = []
    ordering = ["email"]


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
