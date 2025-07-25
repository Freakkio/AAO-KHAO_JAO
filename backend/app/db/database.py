from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.MONGO_DETAILS)
db = client.food_ordering

user_collection = db.get_collection("users")
restaurant_collection = db.get_collection("restaurants")