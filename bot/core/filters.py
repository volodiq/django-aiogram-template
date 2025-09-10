from aiogram import filters, types
from dishka.integrations.aiogram import FromDishka

from .api import UsersAPI


class IsAdmin(filters.BaseFilter):
    async def __call__(
        self,
        message: types.Message,
        users_api_client: FromDishka[UsersAPI],
    ) -> bool:
        user = message.from_user
        if user is None:
            raise ValueError("User is None")

        data = await users_api_client.get_me()
        return data.is_superuser
