import socket
import os
from dotenv import load_dotenv
from datetime import datetime
from app.services.database import get_database
import asyncio

# Load environment variables
load_dotenv()

async def get_local_ip():
    """Returns the Wi-Fi/local network IP address (e.g., 192.168.x.x)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable, just used to determine local IP
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    finally:
        s.close()
    return ip_address

async def save_backend_ip():
    """Save backend IP address to MongoDB"""
    try:
        ip_address = await get_local_ip()
        print(f"🔌 Backend Wi-Fi IP: {ip_address}")

        # Get MongoDB database
        db = await get_database()
        collection = db["network_config"]
        
        # Save to MongoDB
        result = await collection.update_one(
            {"_id": "backend_ip"},
            {"$set": {
                "ip_address": ip_address,
                "last_updated": datetime.utcnow(),
                "hostname": socket.gethostname()
            }},
            upsert=True  # Create if doesn't exist, update if it does
        )
        
        if result.upserted_id:
            print(f"✅ Backend IP saved to MongoDB with ID: {result.upserted_id}")
        else:
            print("✅ Backend IP updated in MongoDB")
            
        return ip_address
        
    except Exception as e:
        print(f"❌ Error saving backend IP to MongoDB: {e}")
        import traceback
        traceback.print_exc()
        return None

# For synchronous usage (if needed)
def save_backend_ip_sync():
    """Synchronous wrapper for the async function"""
    return asyncio.run(save_backend_ip())

# Run if this script is executed directly
if __name__ == "__main__":
    ip = asyncio.run(save_backend_ip())
    if ip:
        print(f"🌐 Successfully saved IP: {ip}")
    else:
        print("❌ Failed to save IP address")