from aiogram import Router, filters, types
from aiogram_dialog import DialogManager, StartMode

from contexts.users.dialogs.menu import dialog as users_menu_dialog
from contexts.users.states import UsersMenuSG


root_router = Router()


@root_router.message(filters.Command("start"))
async def start_command(msg: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(UsersMenuSG.menu, mode=StartMode.RESET_STACK)


root_router.include_routers(
    users_menu_dialog,
)
