from typing import List
from psycopg2.extras import execute_values
from conf.database import Postgres
from .models import Source, Tag, Query, TextData, Statistics, Intention


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

    @classmethod
    def get_intentions(cls) -> List[Intention]:
        statement = """
            SELECT DISTINCT intention FROM text_data;
        """

        with Postgres() as db:
            db.cur.execute(statement)
            results = db.cur.fetchall()
        intentions = [
            Source(id=intention[0], title=intention[0])
            for intention in results
        ]
        return intentions

    @classmethod
    def get(cls, source: str, id: str, **kwargs) -> TextData:
        fields = ("source", "id", "content", "created_at", "intention", )
        statement = f"SELECT {','.join(fields)} FROM text_data WHERE source=%s AND id=%s"
        with Postgres() as db:
            db.cur.execute(statement, (source, id,))
            result = db.cur.fetchone()
        return TextData(**dict(zip(fields, result)))


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
    def get_bulk(cls, tags: List[int]) -> List[Tag]:
        fields = ("id", "title", )
        tag_query_string = f'({",".join(tags)})'
        statement = f"""
            SELECT {",".join(fields)} FROM tag
            WHERE id IN {tag_query_string};
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
            SELECT {",".join(fields)} FROM query
            WHERE id=(SELECT MAX(id) FROM tag);
        """
        with Postgres() as db:
            db.cur.execute(statement)
            result = db.cur.fetchone()
        return Query(**dict(zip(fields, result)))

    @classmethod
    def get_by_query(cls, query: str) -> Query:
        fields = ("id", "query", )
        statement = f"""
            SELECT {",".join(fields)} FROM query
            WHERE query=%s;
        """
        with Postgres() as db:
            db.cur.execute(statement, (query, ))
            result = db.cur.fetchone()
        if not result:
            return None
        return Query(**dict(zip(fields, result)))

    @classmethod
    def create(cls, query) -> Query:
        statement = "INSERT INTO query (query) VALUES (%s);"
        with Postgres() as db:
            db.cur.execute(statement, (query, ))
        return cls.get_last_entry()

    @classmethod
    def get_or_create(cls, sources: List[str], tags: List[int], intentions: List[str]) -> Query:
        raw_query = (
            f"sources={str(list(sorted(sources)))},"
            f"tags={str(list(sorted(tags)))},"
            f"intentions={str(list(sorted(intentions)))}"
        )
        query = cls.get_by_query(query=raw_query)
        if query:
            return query
        return cls.create(query=raw_query)


class LabelManager:
    @classmethod
    def get_next(cls, sources: List[str], intentions: List[str], query: Query) -> TextData:
        fields = ("source", "id", "content", "created_at", "intention", )
        source_query_string = '({})'.format(",".join([f"'{source}'" for source in sources]))
        intention_query_string = '({})'.format(",".join([f"'{intention}'" for intention in intentions]))
        statement = f"""
            SELECT {",".join(fields)} FROM text_data
            WHERE source IN {source_query_string} AND intention IN {intention_query_string}
            AND id NOT IN (
                SELECT id FROM already_labeled
                WHERE query=%s
            )
            LIMIT 1;
        """
        with Postgres() as db:
            db.cur.execute(statement, (query.id, ))
            result = db.cur.fetchone()
        if not result:
            return None
        return TextData(**dict(zip(fields, result)))

    @classmethod
    def create_bulk(cls, text_data: TextData, tags: List[int]) -> None:
        unified_value = [(tag, text_data.source, text_data.id) for tag in tags]
        statement = """
            INSERT INTO label (tag, source, id)
            VALUES %s
            ON CONFLICT (tag, source, id) DO NOTHING;
        """
        with Postgres() as db:
            execute_values(cur=db.cur, sql=statement, argslist=unified_value)
        return None


class AlreadyLabeledManager:
    @classmethod
    def create(cls, query: Query, text_data: TextData) -> None:
        statement = """
            INSERT INTO already_labeled (query, source, id)
            VALUES (%s, %s, %s)
            ON CONFLICT (query, source, id) DO NOTHING;
        """
        with Postgres() as db:
            db.cur.execute(statement, (query.id, text_data.source, text_data.id, ))


class StatisticsManager:
    @classmethod
    def get(cls, sources: List[str], tags: List[int], query: Query) -> Statistics:
        source_query_string = '({})'.format(",".join([f"'{source}'" for source in sources]))
        tag_query_string = '({})'.format(",".join(tags))
        data_count_statement = f"""
            SELECT COUNT(*) FROM text_data
            WHERE source IN {source_query_string};
        """
        already_labeled_statement = "SELECT COUNT(*) FROM already_labeled WHERE query=%s"
        selection_match_statement = f"""
            SELECT COUNT(*) FROM label WHERE tag IN {tag_query_string}
        """
        with Postgres() as db:
            db.cur.execute(data_count_statement)
            data_count_result = db.cur.fetchone()[0]
            db.cur.execute(already_labeled_statement, (query.id, ))
            already_labeled_result = db.cur.fetchone()[0]
            db.cur.execute(selection_match_statement)
            selection_match_result = db.cur.fetchone()[0]
        return Statistics(
            text_data=data_count_result,
            already_labeled=already_labeled_result,
            matches=selection_match_result
        )
