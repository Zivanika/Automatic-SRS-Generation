import os
from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    client: MongoClient = None
    db: Database = None

def get_database() -> Database:
    """
    Get MongoDB database instance
    Creates connection if not exists
    """
    if MongoDB.db is not None:
        return MongoDB.db
    
    try:
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI environment variable is not set")
        
        # Create MongoDB client
        MongoDB.client = MongoClient(mongo_uri)
        
        # Get database name from URI or use default
        db_name = os.getenv("MONGO_DB_NAME", "test")
        MongoDB.db = MongoDB.client[db_name]
        
        # Test connection
        MongoDB.client.admin.command('ping')
        print("[+] MongoDB Connected Successfully")
        
        return MongoDB.db
    except Exception as e:
        print(f"[-] Database Connection Failed: {e}")
        raise

def close_database():
    """Close MongoDB connection"""
    if MongoDB.client:
        MongoDB.client.close()
        MongoDB.client = None
        MongoDB.db = None
        print("[+] MongoDB Connection Closed")

