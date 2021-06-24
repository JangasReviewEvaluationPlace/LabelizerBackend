from typing import Optional
from enum import Enum
from flask import request
from flask_restx import Resource
from .models import Token
from .managers import TokenManager


class AuthMethod(Enum):
    ALL = "all"
    COOKIE = "cookie"
    HEADER = "header"


class AuthRequiredResource(Resource):
    auth_method = AuthMethod.ALL

    def dispatch_request(self, *args, **kwargs):
        token = self.authenticate_user()
        if not token:
            return {}, 401

        self.auth_user = token.auth_user
        return super().dispatch_request(*args, **kwargs)

    def authenticate_user(self) -> Optional[Token]:
        if self.auth_method in (AuthMethod.ALL, AuthMethod.COOKIE):
            token = request.cookies.get("AuthToken", type=str)
        if self.auth_method in (AuthMethod.ALL, AuthMethod.HEADER):
            if not token:
                token = request.headers.get("AuthToken", type=str)

        return TokenManager.get(token=token)
