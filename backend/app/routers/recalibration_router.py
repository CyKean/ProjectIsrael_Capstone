from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, Union
from bson import ObjectId

# Use your specific import
from app.services.database import get_database

# Base configuration model with common fields
class BaseConfiguration(BaseModel):
    device: str
    deviceType: str
    wifiSSID: str
    wifiPassword: str
    lastUpdated: Optional[Dict[str, Any]] = None
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

# Router setup
router = APIRouter(prefix="/api", tags=["configurations"])

@router.get("/{device}")
async def get_configuration(device: str, db = Depends(get_database)):
    """
    Get configuration for a specific device
    """
    try:
        collection = db["configurations"]
        config = collection.find_one({"_id": f"{device}Config"})
        
        if not config:
            raise HTTPException(status_code=404, detail="Configuration not found")
        
        # Convert ObjectId to string for JSON serialization
        if "id" in config:
            config["id"] = str(config["id"])
        return {"config": config}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/{device}")
async def create_configuration(device: str, config_data: Dict[str, Any], db = Depends(get_database)):
    """
    Create or update configuration for a device
    """
    try:
        collection = db["configurations"]
        
        # Prepare the document with _id as deviceConfig
        config_doc = {
            "_id": f"{device}Config",
            **config_data,
            "updated_at": datetime.utcnow()
        }
        
        # Use replace_one with upsert to maintain the _id field structure
        result = collection.replace_one(
            {"_id": f"{device}Config"},
            config_doc,
            upsert=True
        )
        
        return {"message": "Configuration saved successfully", "id": f"{device}Config"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/{device}")
async def update_configuration(device: str, config_data: Dict[str, Any], db = Depends(get_database)):
    """
    Update configuration for a device (partial update)
    """
    try:
        collection = db["configurations"]
        
        # Add updated_at timestamp
        config_data["updated_at"] = datetime.utcnow()
        
        result = collection.update_one(
            {"_id": f"{device}Config"},
            {"$set": config_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Configuration not found")
            
        return {"message": "Configuration updated successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/{device}")
async def delete_configuration(device: str, db = Depends(get_database)):
    """
    Delete configuration for a device
    """
    try:
        collection = db["configurations"]
        result = collection.delete_one({"_id": f"{device}Config"})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Configuration not found")
            
        return {"message": "Configuration deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("")
async def get_all_configurations(db = Depends(get_database)):
    """
    Get all configurations
    """
    try:
        collection = db["configurations"]
        configs = []
        
        for config in collection.find():
            # Convert ObjectId to string if it exists
            if "id" in config:
                config["id"] = str(config["id"])
            configs.append(config)
            
        return {"configurations": configs}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/type/{device_type}")
async def get_configurations_by_type(device_type: str, db = Depends(get_database)):
    """
    Get all configurations of a specific device type
    """
    try:
        collection = db["configurations"]
        configs = []
        
        for config in collection.find({"deviceType": device_type}):
            if "id" in config:
                config["id"] = str(config["id"])
            configs.append(config)
            
        return {"configurations": configs}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

@router.get("/network/backend")
async def get_network_details(db = Depends(get_database)):
    """
    Get network details from MongoDB
    """
    try:
        # If using Motor (async MongoDB driver), use await
        network_collection = db["network"]
        network_data = await network_collection.find_one({"_id": "backend"})
        
        if not network_data:
            return {"ip_address": ""}
        
        return {"ip_address": network_data.get("ip_address", "")}
        
    except Exception as e:
        print(f"Error in get_network_details: {str(e)}")
        return {"ip_address": ""}

@router.put("/network/backend")
async def update_network_details(
    network_data: Dict[str, Any],
    db = Depends(get_database)
):
    """
    Update network details in MongoDB
    """
    try:
        network_collection = db["network"]
        
        # For Motor (async), use await
        result = await network_collection.update_one(
            {"_id": "backend"},
            {
                "$set": {
                    "ip_address": network_data.get("ip_address", ""),
                    "updated_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        
        return {"message": "Network details updated successfully", "modified_count": result.modified_count}
        
    except Exception as e:
        print(f"Error in update_network_details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating network details: {str(e)}")