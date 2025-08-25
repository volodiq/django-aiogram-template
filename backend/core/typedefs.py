from django.http.request import HttpRequest

from core.models.user import UserModel


class AuthedRequest(HttpRequest):
    auth: UserModel
