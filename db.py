import datetime
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize MongoDB client
client = MongoClient(os.getenv("MONGO_URI"))  # Ensure this matches your environment variable
db = client["aibotdata"]  # Replace with your desired database name
users_collection = db["users"]  # Users collection
chat_logs_collection = db["chat_logs"]  # Chat logs collection

def store_chat_log(user_id, message, response):
    """
    Stores chat logs in MongoDB Atlas.
    """
    chat_log = {
        "user_id": user_id,
        "message": message,
        "response": response,
        "timestamp": datetime.datetime.now().isoformat()  # Add timestamp
    }
    chat_logs_collection.insert_one(chat_log)

def create_user_entry(user_id, user_name):
    """
    Creates an entry for a new user in MongoDB Atlas.
    """
    # Check if the user already exists
    if not users_collection.find_one({"user_id": user_id}):
        user_entry = {
            "user_id": user_id,
            "user_name": user_name,
            "created_at": datetime.datetime.now().isoformat()  # Add timestamp
        }
        users_collection.insert_one(user_entry)

def store_userdata_log(user_id, user_name, message, response):
    """
    Stores user data and chat logs.
    """
    create_user_entry(user_id, user_name)  # Create user entry if it doesn't exist
    store_chat_log(user_id, message, response)  # Store chat log
