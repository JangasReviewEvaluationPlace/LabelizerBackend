import uuid
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from .models import AuthUser, Token
from conf.database import Postgres
from conf.configs import SALTED_PASSWORD_LENGTH


class AuthUserManager:
    @classmethod
    def get(cls, id: int) -> AuthUser:
        fields = ("id", "email", "password", )
        statement = f"""SELECT {','.join(fields)} FROM auth_user WHERE id=%s;"""
        with Postgres() as db:
            db.cur.execute(statement, (id, ))
            result = db.cur.fetchone()
        return AuthUser(**dict(zip(fields, result)))

    @classmethod
    def get_latest_entry(cls) -> AuthUser:
        fields = ("id", "email", "password", )
        statement = f"""
            SELECT {','.join(fields)} FROM auth_user
            WHERE id=(SELECT MAX(id) FROM auth_user);
        """
        with Postgres() as db:
            db.cur.execute(statement)
            result = db.cur.fetchone()
        return AuthUser(**dict(zip(fields, result)))

    @classmethod
    def create(cls, email: str, password: str) -> AuthUser:
        statement = "INSERT INTO auth_user (email, password) VALUES (%s, %s);"
        with Postgres() as db:
            db.cur.execute(statement, (
                email,
                generate_password_hash(
                    password=password,
                    method="sha256",
                    salt_length=SALTED_PASSWORD_LENGTH
                )
            ))
        return cls.get_latest_entry()

    @classmethod
    def auth(cls, email: str, password: str) -> Optional[AuthUser]:
        fields = ("id", "email", "password", )
        statement = f"SELECT {','.join(fields)} FROM auth_user WHERE email=%s;"
        with Postgres() as db:
            db.cur.execute(statement, (email, ))
            result = db.cur.fetchone()
        if not result:
            return None
        auth_user = AuthUser(**dict(zip(fields, result)))
        if not check_password_hash(auth_user.password, password):
            return None
        return auth_user


class TokenManager:
    @classmethod
    def create(cls, auth_user: AuthUser) -> Token:
        statement = """
            INSERT INTO token (key, auth_user)
            VALUES (%s, %s)
            ON CONFLICT (auth_user) DO UPDATE SET key=%s
        """
        token = uuid.uuid4().hex
        with Postgres() as db:
            db.cur.execute(statement, (token, auth_user.id, token, ))
        return cls.get(token=token)

    @classmethod
    def get(cls, token: str, auth_user: Optional[AuthUser] = None) -> Optional[Token]:
        fields = ("key", "auth_user", "timestamp", )
        statement = f"SELECT {','.join(fields)} FROM token WHERE key=%s"
        with Postgres() as db:
            db.cur.execute(statement, (token, ))
            result = db.cur.fetchone()
        if not result:
            return None
        token_dict = dict(zip(fields, result))
        if not auth_user:
            auth_user = AuthUserManager.get(id=token_dict["auth_user"])

        return Token(
            key=token,
            auth_user=auth_user,
            timestamp=token_dict["timestamp"]
        )
