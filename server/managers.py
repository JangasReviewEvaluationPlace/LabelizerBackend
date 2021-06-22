from typing import List
from .database import Postgres
from .models import Source, Tag


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
    def get_last_entry(cls):
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
