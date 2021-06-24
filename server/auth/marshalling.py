from flask_restx import fields
from conf.configs import api


auth_user_response_marshalling = api.model("AuthUser", {
    "id": fields.Integer(),
    "email": fields.String()
})

auth_user_marshalling = api.model("AuthUser", {
    "email": fields.String(required=True),
    "password": fields.String(required=True)
})
