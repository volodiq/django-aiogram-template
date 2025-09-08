from providers.api import API

from . import dtos


class UsersAPI(API):
    async def get_me(self):
        return await self.api_client.get("/users/me/", response_dto=dtos.UsersMeDTO)
