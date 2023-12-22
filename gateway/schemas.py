from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from fastapi import File, UploadFile, Form
from dataclasses import dataclass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    channelID: str
    channelName: str
    created_at: datetime

    class Config:
        form_attribtes = True

@dataclass
class CreateUserForm:
    email: EmailStr = Form(...)
    password: str = Form(...)
    channelID: str = Form(...)
    channelName: str = Form(...)
    avatar: UploadFile = File(...)

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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

@dataclass
class CreatePostForm:
    title: str = Form(...)
    description: str = Form(...)
    video: UploadFile = File(...)

@dataclass
class UpdatePostForm:
    title: Optional[str] = Form(None)
    description: Optional[str] = Form(None)
    video: Optional[UploadFile] = File(None)

class Post(BaseModel):
    title: str
    description: str
    thumbnail: str
    video: str
    created_at: datetime

class PostResponse(BaseModel):
    post: Post
    avatar: str
    channelID: str