from contextlib import asynccontextmanager
from typing import AsyncIterator, Self

from dependency_injector import containers, providers, resources
from httpx import AsyncClient


class HTTPClient(resources.AsyncResource):
    async def init(self):
        return AsyncClient()

    async def shutdown(self, http_client):
        await http_client.aclose()


class BaseContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    @classmethod
    @asynccontextmanager
    async def start(cls, tg_id: int) -> AsyncIterator[Self]:
        container = cls()
        container.config.from_dict({"tg_id": tg_id})
        await container.init_resources()  # type: ignore
        try:
            yield container
        finally:
            await container.shutdown_resources()  # type: ignore
