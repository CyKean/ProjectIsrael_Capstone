from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "projectisrael_db")

# Async client
client = None
database = None

# Initialize the database connection
def init_database():
    global client, database
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        database = client[DATABASE_NAME]
        print(f"✅ Connected to MongoDB: {DATABASE_NAME}")
        return database
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise e

# Get database instance
async def get_database():
    global database
    if database is None:
        database = init_database()
    return database

# Sync client (for operations that don't need async)
def get_sync_database():
    sync_client = MongoClient(MONGO_URI)
    return sync_client[DATABASE_NAME]

# Close database connection
async def close_database():
    global client
    if client:
        client.close()
        print("✅ MongoDB connection closed")