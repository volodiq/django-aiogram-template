from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from contexts.users.api import router as users_router
from core.auth import bot_auth


api = NinjaAPI(auth=bot_auth)

api.add_router("/users", router=users_router, tags=["Users"])

# Connect urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
