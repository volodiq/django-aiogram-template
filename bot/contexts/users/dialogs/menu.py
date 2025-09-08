from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets import text
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.api import UsersAPI

from ..states import UsersMenuSG


@inject
async def menu_getter(dialog_manager: DialogManager, api: FromDishka[UsersAPI], *args, **kwargs):
    data = await api.get_me()

    return {
        "greet_msg": f"{data}",
    }


menu = Window(
    text.Format("{greet_msg}"),
    getter=menu_getter,
    state=UsersMenuSG.menu,
)

dialog = Dialog(
    menu,
)
