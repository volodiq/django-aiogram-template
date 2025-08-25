from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, tg_id: int, password: str, **extra_fields):
        user = self.model(tg_id=tg_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, tg_id: int, password: str, **extra_fields):
        extra_fields.update({"is_staff": True})
        extra_fields.update({"is_superuser": True})
        return self.create_user(tg_id, password, **extra_fields)


class UserModel(AbstractBaseUser, PermissionsMixin):
    tg_id: int = models.BigIntegerField(
        verbose_name="Telegram ID",
        unique=True,
        db_index=True,
    )  # type: ignore

    is_staff: bool = models.BooleanField(default=False)  # type: ignore

    USERNAME_FIELD = "tg_id"

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"Пользователь {self.tg_id}"
