from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Comment(BaseModel):
    id: str
    user_id: str
    post_id: str
    reply_to_id: Optional[str] = None
    content: str
    likes: int
    dislikes: int
    date_created: datetime
    date_modified: datetime


class CommentIn(BaseModel):
    reply_to_id: Optional[str] = None
    content: str
