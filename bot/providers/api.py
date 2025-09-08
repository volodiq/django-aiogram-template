from dataclasses import dataclass, field
from functools import wraps
import hmac
from typing import Any, TypeVar, overload

from httpx import AsyncClient, NetworkError, Response
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


@dataclass
class APIClient:
    tg_id: int
    http_client: AsyncClient

    def _generate_auth_header(self) -> str:
        tg_id_sign = hmac.new(
            key=env.secret_key.encode(),
            msg=str(self.tg_id).encode(),
            digestmod="sha256",
        ).hexdigest()
        return f"Bearer {self.tg_id}:{tg_id_sign}"

    def _add_auth_header(self, headers: dict | None = None) -> dict:
        inited_headers = headers.copy() if headers else {}
        auth_header = self._generate_auth_header()
        inited_headers.update({"Authorization": auth_header})
        return inited_headers

    @staticmethod
    def _process_response(
        path: str,
        response_dto: type[DTO] | None,
        response: Response,
    ) -> DTO | None:
        try:
            data = response.json()
        except ValueError:
            if response.is_success:
                if response_dto is None:
                    return None

                log.error(
                    "Empty response, but DTO specified. Path: {path}. Status code: {status_code}",
                    status_code=response.status_code,
                    path=path,
                )
                raise APIEmptyResponseError(path=path)

            log.error(
                "Invalid status code. Path: {path}. Status code: {status_code}",
                status_code=response.status_code,
                path=path,
            )
            raise APIInvalidStatusCodeError(path=path, status_code=response.status_code)

        if response.is_success:
            if response_dto is None:
                return None
            return response_dto.model_validate(data)

        log.error(
            "Invalid status code. Status code: {status_code}. Path: {path}. Data: {data}",
            status_code=response.status_code,
            path=path,
            data=data,
        )
        raise APIInvalidStatusCodeError(path=path, status_code=response.status_code, data=data)

    @staticmethod
    def request_wrapper(method):
        @wraps(method)
        async def wrapped(*args, **kwargs):
            self = args[0]
            path = args[1]

            headers = kwargs.get("headers", None)
            inited_headers = self._add_auth_header(headers)
            kwargs.update({"headers": inited_headers})

            try:
                response: Response = await method(*args, **kwargs)
            except NetworkError as e:
                log.error("NetworkError while request. Path: {path}", path=path)
                raise APIUnavailableError(path=path) from e

            response_dto: BaseModel | None = kwargs.get("response_dto")
            return self._process_response(
                path=path,
                response_dto=response_dto,
                response=response,
            )

        return wrapped

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

    @request_wrapper
    async def get(
        self,
        path: str,
        *,
        response_dto: type[DTO] | None = None,
        headers: dict | None = None,
        params: dict | None = None,
    ) -> Any:
        return await self.http_client.get(
            f"{env.api_base_url}{path}",
            params=params,
            headers=headers,
            timeout=10,
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

    @request_wrapper
    async def post(
        self,
        path: str,
        *,
        response_dto: type[DTO] | None = None,
        headers: dict | None = None,
        json: dict | None = None,
    ) -> Any:
        return await self.http_client.post(
            f"{env.api_base_url}{path}",
            json=json,
            headers=headers,
            timeout=10,
        )


@dataclass
class API:
    api_client: APIClient
