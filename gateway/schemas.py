from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

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