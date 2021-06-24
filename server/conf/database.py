from contextlib import AbstractContextManager

import psycopg2
from .configs import POSTGRES_CONFIGS


class Postgres(AbstractContextManager):
    def __enter__(self):
        self.con = psycopg2.connect(**POSTGRES_CONFIGS)
        self.con.autocommit = True
        self.cur = self.con.cursor()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()
