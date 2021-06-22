from os import name
from flask import request
from flask_restx import Resource
from .managers import TextDataManager, TagManager, LabelManager
from .marshalling import source_marshalling, tag_marshalling, \
    tag_create_marshalling, label_marshalling
from .configs import api


namespace = api.namespace("/")


@namespace.route("/sources")
class SourceAPI(Resource):
    @namespace.marshal_with(source_marshalling)
    def get(self):
        return TextDataManager.get_sources()


@namespace.route("/tags")
class TagAPI(Resource):
    @namespace.marshal_with(tag_marshalling)
    def get(self):
        return TagManager.get_all()

    @namespace.marshal_with(tag_marshalling, code=201)
    @namespace.expect(tag_create_marshalling, validate=True)
    def post(self):
        return TagManager.create(**namespace.payload)


@namespace.route("/query")
class LabelAPI(Resource):
    @namespace.marshal_with(label_marshalling)
    def get(self):
        sources = request.args.getlist('sources')
        tags = request.args.getlist('tags')
        return LabelManager.get_next(sources=sources, tags=tags)
