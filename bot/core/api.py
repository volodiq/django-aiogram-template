from providers.api import BaseApiClient

from . import dtos


class UsersApiClient(BaseApiClient):
    async def get_me(self):
        return await self.get("/users/me/", response_dto=dtos.UsersMeDTO)
