from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Category(BaseModel):
    id: str
    name: str
    description: str
    topics: List[str]
    date_created: datetime
    date_modified: datetime


class CategoryIn(BaseModel):
    name: str
    description: str
    topics: List[str]


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    topics: Optional[List[str]] = None
