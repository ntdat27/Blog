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
    like: int = Field(default=0)