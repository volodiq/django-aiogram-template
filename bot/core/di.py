from typing import AsyncIterable

from aiogram.dispatcher.middlewares.user_context import EVENT_CONTEXT_KEY, EventContext
from dishka import Provider, Scope, provide
from dishka.integrations.aiogram import AiogramMiddlewareData
from httpx import AsyncClient

from providers.api import APIClient

from .api import UsersAPI


provider = Provider(scope=Scope.REQUEST)
provider.provide(UsersAPI)


class HTTPClientProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_http_client(self) -> AsyncIterable[AsyncClient]:
        client = AsyncClient()
        yield client
        await client.aclose()


class APIClientProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_api_client(
        self,
        http_client: AsyncClient,
        middleware_data: AiogramMiddlewareData,
    ) -> APIClient:
        event_context: EventContext = middleware_data[EVENT_CONTEXT_KEY]
        user_id = event_context.user_id
        if user_id is None:
            raise ValueError("User Telegram ID is None")

        return APIClient(
            tg_id=user_id,
            http_client=http_client,
        )
