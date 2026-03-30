from pydantic import BaseModel, Field , EmailStr

import uuid

class UserCreate(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6)

class UserInDB(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str