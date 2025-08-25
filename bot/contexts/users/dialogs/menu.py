from aiogram.dispatcher.middlewares.user_context import EVENT_CONTEXT_KEY
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets import text

from core.di import UsersContainer

from ..states import UsersMenuSG


async def menu_getter(dialog_manager: DialogManager, *args, **kwargs):
    user_id: int = dialog_manager.middleware_data[EVENT_CONTEXT_KEY].user_id

    async with UsersContainer.start(user_id) as container:
        api = await container.users_api_client()
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
