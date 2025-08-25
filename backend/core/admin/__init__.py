from django.contrib import admin
from django.contrib.auth.models import Group

from .user import UserModelAdmin


admin.site.unregister(Group)


__all__ = ("UserModelAdmin",)
