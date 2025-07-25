from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel

from app.db.database import restaurant_collection
from app.schemas.restaurant import RestaurantOut, RestaurantDetailOut
from app.models.restaurant import MenuItem

router = APIRouter()

# --- NEW RESPONSE MODELS FOR OUR RECOMMENDATION ---
class RecommendationResponse(BaseModel):
    searched_item: MenuItem
    healthier_alternatives: List[MenuItem]

# --- CORRECTED AND SIMPLIFIED ENDPOINTS ---

@router.get("/", response_model=List[RestaurantOut])
async def get_all_restaurants(cuisine: Optional[str] = None):
    query = {}
    if cuisine:
        query["cuisine_type"] = {"$regex": cuisine, "$options": "i"}
    restaurants = list(restaurant_collection.find(query))
    return restaurants

@router.get("/{restaurant_id}", response_model=RestaurantDetailOut)
async def get_restaurant_details(restaurant_id: str):
    try:
        oid = ObjectId(restaurant_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    restaurant = restaurant_collection.find_one({"_id": oid})
    if restaurant:
        return restaurant
    raise HTTPException(status_code=404, detail=f"Restaurant with id {restaurant_id} not found")


# --- THE COMPLETELY REWRITTEN RECOMMENDATION ENDPOINT ---
@router.get("/search/healthy-alternatives/", response_model=RecommendationResponse)
async def get_healthy_alternatives(food_item: str):
    """
    Suggests healthier alternatives to a searched high-calorie food.
    This is a robust, corrected version.
    """
    # 1. Find the item the user searched for
    searched_item_cursor = restaurant_collection.aggregate([
        {"$unwind": "$menu"},
        {"$match": {"menu.name": {"$regex": food_item, "$options": "i"}}},
        {"$limit": 1}
    ])
    
    found_items = list(searched_item_cursor)
    if not found_items:
        raise HTTPException(status_code=404, detail=f"Could not find nutritional info for '{food_item}'")

    searched_item_data = found_items[0]['menu']
    searched_calories = searched_item_data['nutritional_info']['calories']

    # 2. Find all items that are significantly healthier
    # We relax the criteria to ensure we find something
    calorie_threshold = searched_calories * 0.8  # Look for items with at least 20% fewer calories

    alternatives_cursor = restaurant_collection.aggregate([
        {"$unwind": "$menu"},
        {"$match": {
            "menu.nutritional_info.calories": {"$lt": calorie_threshold},
            # Ensure we don't recommend the same item
            "menu.name": {"$not": {"$regex": food_item, "$options": "i"}}
        }},
        {"$limit": 5}, # Limit to 5 alternatives
        {"$replaceRoot": {"newRoot": "$menu"}} # Reshape the document to just be the menu item
    ])
    
    alternatives_list = list(alternatives_cursor)

    # 3. Always return a valid response object
    # Pydantic will handle the serialization correctly.
    return {
        "searched_item": searched_item_data,
        "healthier_alternatives": alternatives_list
    }