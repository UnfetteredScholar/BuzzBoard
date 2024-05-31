from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel


class UserStatus(str, Enum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    DISABLED = "disabled"


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class User(BaseModel):
    id: str
    username: str
    email: str
    password: str
    status: UserStatus
    role: Role
    subscribed: List[str]
    date_created: datetime
    date_modified: datetime


class UserIn(BaseModel):
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    id: str
    username: str
    email: str
    role: Role
    subscribed: List[str]
    status: UserStatus
    date_created: datetime
    date_modified: datetime
