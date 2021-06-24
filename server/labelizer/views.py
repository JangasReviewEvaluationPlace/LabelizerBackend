from flask import request
from auth.validator import AuthRequiredResource
from .managers import TextDataManager, TagManager, LabelManager, QueryManager, \
    AlreadyLabeledManager, StatisticsManager
from .marshalling import source_marshalling, tag_marshalling, \
    tag_create_marshalling, label_marshalling, label_create_marshalling, \
    statistics_marshalling, intention_marshalling
from conf.configs import api


namespace = api.namespace("/labelizer")


@namespace.route("/")
class DashboardAPI(AuthRequiredResource):
    def get(self):
        return {}, 200


@namespace.route("/sources")
class SourceAPI(AuthRequiredResource):
    @namespace.marshal_with(source_marshalling)
    def get(self):
        return TextDataManager.get_sources()


@namespace.route("/intentions")
class IntentionAPI(AuthRequiredResource):
    @namespace.marshal_with(intention_marshalling)
    def get(self):
        return TextDataManager.get_intentions()


@namespace.route("/tags")
class TagAPI(AuthRequiredResource):
    @namespace.marshal_with(tag_marshalling)
    def get(self):
        tags = request.args.getlist('tags')
        if tags == []:
            return TagManager.get_all()
        return TagManager.get_bulk(tags=tags)

    @namespace.marshal_with(tag_marshalling, code=201)
    @namespace.expect(tag_create_marshalling, validate=True)
    def post(self):
        return TagManager.create(**namespace.payload)


@namespace.route("/label")
class LabelAPI(AuthRequiredResource):
    @namespace.marshal_with(label_marshalling)
    def get(self):
        sources = request.args.getlist('sources')
        tags = request.args.getlist('tags')
        intentions = request.args.getlist('intentions')
        query = QueryManager.get_or_create(sources=sources, tags=tags, intentions=intentions)
        return LabelManager.get_next(sources=sources, intentions=intentions, query=query)

    @namespace.expect(label_create_marshalling, validate=True)
    def post(self):
        text_data = TextDataManager.get(**namespace.payload)
        sources = request.args.getlist('sources')
        tags = request.args.getlist('tags')
        intentions = request.args.getlist('intentions')
        query = QueryManager.get_or_create(sources=sources, tags=tags, intentions=intentions)
        LabelManager.create_bulk(text_data=text_data, tags=tags)
        AlreadyLabeledManager.create(query=query, text_data=text_data)
        return {}


@namespace.route("/statistics")
class StatisticApi(AuthRequiredResource):
    @namespace.marshal_with(statistics_marshalling)
    def get(self):
        sources = request.args.getlist('sources')
        tags = request.args.getlist('tags')
        intentions = request.args.getlist('intentions')
        query = QueryManager.get_or_create(sources=sources, tags=tags, intentions=intentions)
        return StatisticsManager.get(sources=sources, tags=tags, query=query)
