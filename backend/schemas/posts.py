from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class PostSortTypes(str, Enum):
    HOT = "hot"
    NEW = "new"
    TOP = "top"


class Post(BaseModel):
    id: str
    user_id: str
    category_id: str
    category_topic: str
    title: str
    content: str
    post_image_url: Optional[str] = None
    likes: int
    dislikes: int
    comments: int
    date_created: datetime
    date_modified: datetime


class PostIn(BaseModel):
    category_id: str
    category_topic: str
    title: str
    content: str
