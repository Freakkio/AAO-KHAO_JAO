from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class UserProfile(BaseModel):
    calorie_goal: Optional[int] = 2000
    dietary_restrictions: List[str] = []

class UserInDB(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    profile: UserProfile = Field(default_factory=UserProfile)
    order_history: List[str] = []  # List of Order IDs
    favorite_items: List[str] = []  # List of Menu Item IDs