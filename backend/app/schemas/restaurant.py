# backend/app/schemas/restaurant.py

from pydantic import BaseModel, Field, ConfigDict
from typing import List
from app.models.restaurant import MenuItem
from app.models.pyobjectid import PyObjectId

class RestaurantOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: PyObjectId = Field(..., alias="_id")
    name: str
    cuisine_type: str
    rating: float

class RestaurantDetailOut(RestaurantOut):
    menu: List[MenuItem]