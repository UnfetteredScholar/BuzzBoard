from datetime import datetime

from pydantic import BaseModel


class Reaction(BaseModel):
    id: str
    user_id: str
    target_id: str
    is_like: bool
    date_created: datetime
    date_modified: datetime


class ReactionIn(BaseModel):
    target_id: str
    is_like: bool
