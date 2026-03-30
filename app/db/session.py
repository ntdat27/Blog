
from pymongo import MongoClient 
import os

from app.core.config import settings

CONNECTION_STRING = settings.database_url

def create_collection(db, collection_name):
    collection = db[collection_name]
    return collection



try:
    client = MongoClient(CONNECTION_STRING)
    print("Connecte to MongoDB")
    db = client["blog"]
    like_collection = create_collection(db, "likes")
    post_collection = create_collection(db, "posts")
    user_collection = create_collection(db, "users")
    user_collection.create_index("email", unique=True)
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    user_collection = None
    post_collection = None



