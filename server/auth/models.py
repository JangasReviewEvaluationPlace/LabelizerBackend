from dataclasses import dataclass
from datetime import datetime


@dataclass
class AuthUser:
    id: int
    email: str
    password: str = None


@dataclass
class Token:
    key: str
    auth_user: AuthUser
    timestamp: datetime
