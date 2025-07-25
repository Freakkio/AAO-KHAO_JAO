from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.models.user import UserProfile

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    username: str
    email: EmailStr
    profile: UserProfile

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None