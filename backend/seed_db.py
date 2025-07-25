import pymongo
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_DETAILS = os.getenv("MONGO_DETAILS")

try:
    client = pymongo.MongoClient(MONGO_DETAILS)
    db = client.food_ordering
    restaurant_collection = db.get_collection("restaurants")
    print("Successfully connected to MongoDB.")
except pymongo.errors.ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")
    exit()

restaurant_collection.delete_many({})
print("Cleared existing restaurant data.")

restaurants_data = [
    {
        "_id": ObjectId(), "name": "Pizza Palace", "cuisine_type": "Italian", "rating": 4.5,
        "menu": [
            {"_id": ObjectId(), "name": "Cheese Burst Pizza", "description": "Extra cheese, thick crust.", "price": 15.99, "nutritional_info": {"calories": 1200}, "tags": ["high-calorie", "pizza"]},
            {"_id": ObjectId(), "name": "Thin Crust Vegetable Pizza", "description": "Light, crispy, and healthy.", "price": 13.99, "nutritional_info": {"calories": 650}, "tags": ["healthy", "vegetable", "pizza", "thin crust"]}
        ]
    },
    {
        "_id": ObjectId(), "name": "Burger Barn", "cuisine_type": "American", "rating": 4.2,
        "menu": [
            {"_id": ObjectId(), "name": "Double Bacon Cheeseburger", "description": "Two patties, bacon, and cheese.", "price": 12.99, "nutritional_info": {"calories": 1500}, "tags": ["high-calorie", "burger"]},
            {"_id": ObjectId(), "name": "Grilled Chicken Sandwich", "description": "Healthy grilled chicken.", "price": 10.99, "nutritional_info": {"calories": 550}, "tags": ["healthy", "grilled", "chicken"]}
        ]
    },
    {
        "_id": ObjectId(), "name": "The Green Leaf", "cuisine_type": "Healthy", "rating": 4.8,
        "menu": [
            {"_id": ObjectId(), "name": "Quinoa Power Bowl", "description": "Superfoods to fuel your day.", "price": 11.50, "nutritional_info": {"calories": 480}, "tags": ["healthy", "vegan", "salad"]},
            {"_id": ObjectId(), "name": "Grilled Salmon Salad", "description": "Omega-3 rich and delicious.", "price": 14.99, "nutritional_info": {"calories": 520}, "tags": ["healthy", "grilled", "salad"]}
        ]
    }
]

restaurant_collection.insert_many(restaurants_data)
print(f"Successfully seeded {len(restaurants_data)} restaurants.")
client.close()