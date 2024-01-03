from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from fastapi import File, UploadFile, Form
from dataclasses import dataclass

@dataclass
class CreateUserForm:
    email: EmailStr = Form(...)
    password: str = Form(...)
    channelID: str = Form(...)
    channelName: str = Form(...)
    avatar: UploadFile = File(...)
    channelDescription: Optional[str] = Form(None)

@dataclass
class LoginUserForm:
    email: EmailStr = Form(...)
    password: str = Form(...)

@dataclass
class UpdateUserForm:
    email: Optional[str] = Form(None)
    password: Optional[str] = Form(None)
    channelID: Optional[str] = Form(None)
    channelName: Optional[str] = Form(None)
    avatar: Optional[UploadFile] = File(None)
    channelDescription: Optional[str] = Form(None)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

@dataclass
class CreatePostForm:
    title: str = Form(...)
    description: str = Form(...)
    category: str = Form(...)
    video: UploadFile = File(...)

@dataclass
class UpdatePostForm:
    title: Optional[str] = Form(None)
    description: Optional[str] = Form(None)
    category: Optional[str] = Form(None)
    video: Optional[UploadFile] = File(None)

class UserResponseWithPost(BaseModel):
    channelName: str
    channelID: str
    avatar: str

class Post(BaseModel):
    id: int
    title: str
    description: str
    thumbnail: str
    video: str
    created_at: datetime
    owner: UserResponseWithPost


class SinglePostResponse(Post):
    owner: UserResponseWithPost
    likes: int
    dislikes: int
    shares: int
    liked: bool
    disliked: bool
    shared: bool

class UserResponse(BaseModel):
    channelName: str
    channelID: str
    avatar: str
    channelDescription: str | None

class CreatePostMetric(BaseModel):
    liked: bool
    disliked: bool
    shared: bool