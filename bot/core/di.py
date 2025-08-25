from typing import Awaitable

from dependency_injector import providers

from providers.di import BaseContainer, HTTPClient

from .api import UsersApiClient


class UsersContainer(BaseContainer):
    config = providers.Configuration()
    http_client = providers.Resource(HTTPClient)

    users_api_client = providers.Factory[Awaitable[UsersApiClient]](
        UsersApiClient,  # type: ignore
        tg_id=config.tg_id,
        http_client=http_client,
    )
