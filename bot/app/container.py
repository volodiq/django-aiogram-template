from dishka import make_async_container
from dishka.integrations.aiogram import AiogramProvider

from core.di import APIClientProvider, HTTPClientProvider, provider as core_provider


container = make_async_container(
    core_provider,
    APIClientProvider(),
    HTTPClientProvider(),
    AiogramProvider(),
)
