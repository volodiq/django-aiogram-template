from django.contrib import admin
from unfold.admin import ModelAdmin

from core.models.user import UserModel


@admin.register(UserModel)
class UserModelAdmin(ModelAdmin):
    list_display = [
        "tg_id",
        "is_staff",
    ]

    exclude = [
        "password",
        "last_login",
        "groups",
        "user_permissions",
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
