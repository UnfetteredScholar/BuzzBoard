from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class UserStatus(str, Enum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    DISABLED = "disabled"


class User(BaseModel):
    id: str
    username: str
    email: str
    password: str
    status: UserStatus
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
    status: UserStatus
    date_created: datetime
    date_modified: datetime
