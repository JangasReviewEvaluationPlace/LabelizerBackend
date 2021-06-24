from flask_restx import fields
from conf.configs import api


source_marshalling = api.model("Source", {
    "id": fields.String(),
    "title": fields.String()
})

intention_marshalling = api.model("Intention", {
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

label_marshalling = api.model("Label", {
    "source": fields.String(),
    "id": fields.String(),
    "content": fields.String()
})

label_create_marshalling = api.model("Label", {
    "source": fields.String(required=True),
    "id": fields.String(required=True),
    "tags": fields.List(fields.Integer(), required=True)
})

statistics_marshalling = api.model("Statistics", {
    "text_data": fields.Integer(),
    "already_labeled": fields.Integer(),
    "matches": fields.Integer(),
})
