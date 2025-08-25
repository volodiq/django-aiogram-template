import hmac

from django.http import HttpRequest
from ninja.errors import AuthenticationError

from core.models.user import UserModel
from providers import env


# Helpers


def extract_auth_payload(request: HttpRequest) -> str:
    auth = request.headers.get("Authorization")
    if not auth:
        raise ValueError("Authorization header not found")
    auth = auth.replace("Bearer ", "")
    return auth


def parse_auth_payload(auth_payload: str) -> tuple[str, str]:
    tg_id, sep, tg_id_sign = auth_payload.partition(":")
    if not all((tg_id, sep, tg_id_sign)):
        raise ValueError("Invalid auth payload")
    return tg_id, tg_id_sign


def generate_tg_id_sign(tg_id: str) -> str:
    return hmac.new(
        key=env.secret_key.encode(),
        msg=str(tg_id).encode(),
        digestmod="sha256",
    ).hexdigest()


def is_valid_tg_id_sign(tg_id: str, tg_id_sign: str) -> bool:
    real_tg_id_sign = generate_tg_id_sign(tg_id)
    return hmac.compare_digest(real_tg_id_sign, tg_id_sign)


# Auth variants


async def bot_auth(request: HttpRequest):
    try:
        auth_payload = extract_auth_payload(request)
    except ValueError:
        raise AuthenticationError

    try:
        tg_id, tg_id_sign = parse_auth_payload(auth_payload)
    except ValueError:
        raise AuthenticationError

    is_valid_sign = is_valid_tg_id_sign(tg_id, tg_id_sign)
    if not is_valid_sign:
        raise AuthenticationError

    user, _ = await UserModel.objects.aget_or_create(tg_id=tg_id)
    return user


__all__ = ("bot_auth",)
