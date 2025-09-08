from dataclasses import dataclass, field
import hmac
from typing import Any, TypeVar, overload

from httpx import AsyncClient, Auth, NetworkError, Request, Response
from pydantic import BaseModel

from providers import env
from providers.logger import logger as log


@dataclass
class APIError(Exception):
    path: str


class APIEmptyResponseError(APIError):
    """
    Была указана DTO, но ответ API пустой.
    """


class APIUnavailableError(APIError):
    """
    Ошибка доступа к API из за сетевых проблем.
    """


@dataclass
class APIInvalidStatusCodeError(APIError):
    status_code: int
    data: dict | None = field(default=None)


DTO = TypeVar("DTO", bound=BaseModel)


class TelegramHMACAuth(Auth):
    def __init__(self, tg_id: int, secret_key: str) -> None:
        self._auth_header = self._make_header(tg_id, secret_key)

    @staticmethod
    def _make_header(tg_id: int, secret_key: str) -> str:
        signature = hmac.new(
            key=secret_key.encode(),
            msg=str(tg_id).encode(),
            digestmod="sha256",
        ).hexdigest()
        return f"Bearer {tg_id}:{signature}"

    def auth_flow(self, request: Request):
        request.headers["Authorization"] = self._auth_header
        yield request

    async def async_auth_flow(self, request: Request):
        request.headers["Authorization"] = self._auth_header
        yield request


@dataclass
class APIClient:
    tg_id: int
    http_client: AsyncClient

    @staticmethod
    def _process_unsuccessful_response(
        response: Response,
        path: str,
        data: dict | None = None,
    ):
        if data is None:
            log.error(
                "Invalid status code. Path: {path}. Status code: {status_code}",
                status_code=response.status_code,
                path=path,
            )
            raise APIInvalidStatusCodeError(path=path, status_code=response.status_code)
        else:
            log.error(
                "Invalid status code. Status code: {status_code}. Path: {path}. Data: {data}",
                status_code=response.status_code,
                path=path,
                data=data,
            )
            raise APIInvalidStatusCodeError(path=path, status_code=response.status_code, data=data)

    @classmethod
    def _process_empty_response(
        cls,
        path: str,
        response_dto: type[DTO] | None,
        response: Response,
    ):
        if not response.is_success:
            return cls._process_unsuccessful_response(response=response, path=path)

        if response_dto is None:
            return None

        log.error(
            "Empty response, but DTO specified. Path: {path}. Status code: {status_code}",
            status_code=response.status_code,
            path=path,
        )
        raise APIEmptyResponseError(path=path)

    @classmethod
    def _process_response(
        cls,
        path: str,
        response_dto: type[DTO] | None,
        response: Response,
    ) -> DTO | None:
        try:
            data = response.json()
        except ValueError:
            return cls._process_empty_response(
                path=path,
                response_dto=response_dto,
                response=response,
            )

        if not response.is_success:
            return cls._process_unsuccessful_response(response=response, path=path, data=data)

        if response_dto is None:
            return None

        return response_dto.model_validate(data)

    async def _make_request(
        self,
        method: str,
        path: str,
        response_dto: type[DTO] | None = None,
        **kwargs,
    ):
        url = f"{env.api_base_url}{path}"
        try:
            response = await self.http_client.request(
                method,
                url,
                timeout=10,
                auth=TelegramHMACAuth(self.tg_id, env.secret_key),
                **kwargs,
            )
        except NetworkError as e:
            log.error("NetworkError while request. Path: {path}", path=path)
            raise APIUnavailableError(path=path) from e

        return self._process_response(
            path=path,
            response_dto=response_dto,
            response=response,
        )

    # ===============
    # GET Request
    # ===============

    @overload
    async def get(
        self,
        path: str,
        *,
        response_dto: type[DTO],
        headers: dict | None = None,
        params: dict | None = None,
    ) -> DTO: ...

    @overload
    async def get(
        self,
        path: str,
        *,
        response_dto: None = None,
        headers: dict | None = None,
        params: dict | None = None,
    ) -> None: ...

    async def get(
        self,
        path: str,
        *,
        response_dto: type[DTO] | None = None,
        headers: dict | None = None,
        params: dict | None = None,
    ) -> Any:
        return await self._make_request(
            method="GET",
            path=path,
            params=params,
            response_dto=response_dto,
            headers=headers,
        )

    # ===============
    # POST Request
    # ===============

    @overload
    async def post(
        self,
        path: str,
        *,
        response_dto: type[DTO],
        headers: dict | None = None,
        json: dict | None = None,
    ) -> DTO: ...

    @overload
    async def post(
        self,
        path: str,
        *,
        response_dto: None = None,
        headers: dict | None = None,
        json: dict | None = None,
    ) -> None: ...

    async def post(
        self,
        path: str,
        *,
        response_dto: type[DTO] | None = None,
        headers: dict | None = None,
        json: dict | None = None,
    ) -> Any:
        return await self._make_request(
            method="POST",
            path=path,
            response_dto=response_dto,
            json=json,
            headers=headers,
        )


@dataclass
class API:
    api_client: APIClient
