from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class CurrentUserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class PostResponse(PostBase):
    id: int
    created_at: datetime
    # owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class PostVoteResponse(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class Vote(BaseModel):
    post_id: int
