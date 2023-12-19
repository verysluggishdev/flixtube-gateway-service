from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from fastapi import File, UploadFile, Form
from dataclasses import dataclass

from pydantic.types import conint

class UserOut(BaseModel):
    id: int
    email: EmailStr
    channelID: str
    channelName: str
    created_at: datetime

    class Config:
        form_attribtes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    channelID: str
    channelName: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class PostCreate(BaseModel):
    title: str
    description: str
    video: UploadFile = File(...)

    class Config:
        from_attributes = True

class PostResponse(BaseModel):
    title: str
    description: str
    created_at: datetime

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