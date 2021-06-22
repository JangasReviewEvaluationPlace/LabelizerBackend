from typing import List
from .database import Postgres
from .models import Source, Tag, Query, TextData


class TextDataManager:
    @classmethod
    def get_sources(cls) -> List[Source]:
        statement = """
            SELECT DISTINCT source FROM text_data;
        """

        with Postgres() as db:
            db.cur.execute(statement)
            results = db.cur.fetchall()
        sources = [
            Source(id=source[0], title=source[0])
            for source in results
        ]
        return sources


class TagManager:
    @classmethod
    def get(cls, id: int) -> Tag:
        fields = ("id", "title", )
        statement = f'SELECT {",".join(fields)} FROM tag WHERE id=%s;'
        with Postgres() as db:
            db.cur.execute(statement, (id, ))
            result = db.cur.fetchone()
        return Tag(**dict(zip(fields, result)))

    @classmethod
    def get_last_entry(cls) -> Tag:
        fields = ("id", "title", )
        statement = f"""
            SELECT {",".join(fields)} FROM tag
            WHERE id=(SELECT MAX(id) FROM tag);
        """
        with Postgres() as db:
            db.cur.execute(statement)
            result = db.cur.fetchone()
        return Tag(**dict(zip(fields, result)))

    @classmethod
    def get_all(cls) -> List[Tag]:
        fields = ("id", "title", )

        statement = f"""
            SELECT {",".join(fields)} FROM tag;
        """

        with Postgres() as db:
            db.cur.execute(statement)
            results = db.cur.fetchall()

        tags = [
            Tag(**dict(zip(fields, tag)))
            for tag in results
        ]

        return tags

    @classmethod
    def create(cls, title: str) -> Tag:
        statement = "INSERT INTO tag (title) VALUES (%s);"
        with Postgres() as db:
            db.cur.execute(statement, (title, ))
        return cls.get_last_entry()


class QueryManager:
    @classmethod
    def get_last_entry(cls) -> Query:
        fields = ("id", "query", )
        statement = f"""
            SELECT {",".join(fields)} FROM tag
            WHERE id=(SELECT MAX(id) FROM tag);
        """
        with Postgres() as db:
            db.cur.execute(statement)
            result = db.cur.fetchone()
        return Tag(**dict(zip(fields, result)))

    @classmethod
    def get_by_query(cls, query: str) -> Query:
        fields = ("id", "query", )
        statement = f"""
            SELECT {",".join(fields)} FROM tag
            WHERE query=%s;
        """
        with Postgres() as db:
            db.cur.execute(statement, (query, ))
            result = db.cur.fetchone()
        if not result:
            return None
        return Tag(**dict(zip(fields, result)))

    @classmethod
    def create(cls, query) -> Query:
        statement = "INSERT INTO query (query) VALUES (%s);"
        with Postgres() as db:
            db.cur.execute(statement, (query, ))
        return cls.get_last_entry()

    @classmethod
    def get_or_create(cls, query) -> Query:
        query = cls.get_by_query(query=query)
        if query:
            return query
        return cls.create(query=query)


class LabelManager:
    @classmethod
    def get_next(cls, sources, tags) -> TextData:
        fields = ("source", "id", "content", "created_at", "intention", )
        source_query_string = '({})'.format(",".join([f"'{source}'" for source in sources]))
        tag_query_string = f'({",".join(tags)})'
        statement = f"""
            SELECT {",".join(fields)} FROM text_data
            WHERE source IN {source_query_string}
            AND id NOT IN (
                SELECT id FROM label
                WHERE source IN {source_query_string} AND tag IN {tag_query_string}
            )
            LIMIT 1;
        """
        with Postgres() as db:
            db.cur.execute(statement)
            result = db.cur.fetchone()
        if not result:
            return None
        return TextData(**dict(zip(fields, result)))
