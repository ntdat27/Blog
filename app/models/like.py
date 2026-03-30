from pydantic import BaseModel, Field
from datetime import datetime

class LikeCreate(BaseModel):
    post_id: str = Field(...)

class LikeInDB(BaseModel):
    user_email: str = Field(...) 
    post_id: str = Field(...)    
    updated_at: datetime = Field(default_factory=datetime.now) 