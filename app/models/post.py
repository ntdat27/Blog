from datetime import datetime

from pydantic import BaseModel, Field
import uuid


class PostCreate(BaseModel):
    title: str = Field(...)
    content: str = Field(...)

class PostInDB(PostCreate):
    title: str
    content: str
    author: str = Field(...) 
    created_at: datetime = Field(default_factory=datetime.now)
    view_count: int = Field(default=0)
    like: int = Field(default=0)