from datetime import datetime
from pydantic import BaseModel, EmailStr


class Post(BaseModel):
    title: str
    content: str
    published: bool = False


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
