from flask import after_this_request, Response
from flask_restx import Resource
from conf.configs import api
from .managers import AuthUserManager, TokenManager
from .marshalling import auth_user_marshalling, auth_user_response_marshalling


namespace = api.namespace("/auth")


@namespace.route("/registration")
class RegistrationAPI(Resource):
    @namespace.marshal_with(auth_user_response_marshalling, code=201)
    @namespace.expect(auth_user_marshalling)
    def post(self):
        return AuthUserManager.create(**namespace.payload)


@namespace.route("/authentication")
class AuthenticationAPI(Resource):
    @namespace.marshal_with(auth_user_response_marshalling, code=201)
    @namespace.expect(auth_user_marshalling)
    def post(self):
        @after_this_request
        def set_token_cookie(response: Response):
            if response.status_code != 200:
                return response
            key = token.key
            response.set_cookie(
                key="AuthToken",
                value=key,
                samesite="lax"
            )
            return response

        auth_user = AuthUserManager.auth(**namespace.payload)
        if not auth_user:
            return {}, 400
        token = TokenManager.create(auth_user=auth_user)
        return auth_user, 200
