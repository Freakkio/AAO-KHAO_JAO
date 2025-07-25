# backend/app/models/restaurant.py

from pydantic import BaseModel, Field, ConfigDict # <-- Import ConfigDict
from typing import List, Optional
from .pyobjectid import PyObjectId

class NutritionalInfo(BaseModel):
    calories: int
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None

class MenuItem(BaseModel):
    # Allow population by the '_id' alias from MongoDB
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: PyObjectId = Field(..., alias="_id")
    name: str
    description: str
    price: float
    nutritional_info: NutritionalInfo
    tags: List[str] = []

class Restaurant(BaseModel):
    # Allow population by the '_id' alias from MongoDB
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: PyObjectId = Field(..., alias="_id")
    name: str
    cuisine_type: str
    rating: float = Field(..., ge=0, le=5)
    menu: List[MenuItem] = []