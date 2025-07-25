import pymongo
import os
from dotenv import load_dotenv

# --- Configuration ---
# Put the exact food item name you are searching for here
SEARCH_TERM = "Cheese Burst Pizza"
# -------------------

print(f"--- STARTING DEBUG SCRIPT: Searching for '{SEARCH_TERM}' ---")

# Load environment variables from .env file
load_dotenv()
MONGO_DETAILS = os.getenv("MONGO_DETAILS")

if not MONGO_DETAILS:
    print("ERROR: MONGO_DETAILS not found in .env file. Exiting.")
    exit()

# Connect to the database
try:
    client = pymongo.MongoClient(MONGO_DETAILS)
    db = client.food_ordering
    restaurant_collection = db.get_collection("restaurants")
    print("Successfully connected to MongoDB.")
except Exception as e:
    print(f"ERROR: Could not connect to MongoDB: {e}")
    exit()

# The exact same pipeline from your API endpoint
pipeline = [
    {"$unwind": "$menu"},
    {"$match": {"menu.name": {"$regex": SEARCH_TERM, "$options": "i"}}},
    {"$limit": 1}
]

print("\nRunning the following aggregation pipeline:")
print(pipeline)

# Execute the query
results = list(restaurant_collection.aggregate(pipeline))

# --- Report the Results ---
print("\n--- QUERY RESULTS ---")
if not results:
    print("!!! FAILURE: The query returned 0 results. !!!")
    print("This is why you are getting a 404 error.")
    print("Next Steps: Double-check that you have run 'python seed_db.py' successfully.")
else:
    print("!!! SUCCESS: The query found a result! !!!")
    print("Found item:")
    # Pretty print the result
    import json
    from bson.json_util import dumps
    print(json.dumps(json.loads(dumps(results[0])), indent=4))

client.close()
print("\n--- DEBUG SCRIPT FINISHED ---")