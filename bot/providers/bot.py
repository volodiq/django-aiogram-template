from aiogram import Bot

from . import env


bot = Bot(token=env.bot_token)

__all__ = ("bot",)
