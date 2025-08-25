from aiogram import filters, types

from .di import UsersContainer


class IsAdmin(filters.BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        user = message.from_user
        if user is None:
            raise ValueError("User is None")

        async with UsersContainer.start(user.id) as container:
            api = await container.users_api_client()
            data = await api.get_me()
            return data.is_superuser
