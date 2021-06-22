from flask_restx import fields
from .configs import api


source_marshalling = api.model("Source", {
    "id": fields.String(),
    "title": fields.String()
})

tag_marshalling = api.model("Tag", {
    "id": fields.Integer(),
    "title": fields.String()
})

tag_create_marshalling = api.model("Tag", {
    "title": fields.String(required=True)
})
