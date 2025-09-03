from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from app.ml.integrated_prediction import get_integrated_recommendation
from datetime import datetime, timedelta
from app.services.database import get_database
from bson import ObjectId
import os
from dotenv import load_dotenv

router = APIRouter(prefix="/api")

load_dotenv()

class CropInput(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    soilpH: float
    soilMoisture: float
    temperature: float
    humidity: float

class FertilizerRecommendation(BaseModel):
    type: str
    name: str
    base_amount: float
    adjusted_amount: float
    unit: str

class AlternativeCrop(BaseModel):
    crop: str
    confidence: float
    fertilizer: FertilizerRecommendation

class CropPrediction(BaseModel):
    recommendedCrop: str
    successRate: float
    soilCompatibility: float
    growthRate: float
    yieldPotential: float
    fertilizer: FertilizerRecommendation
    alternativeOptions: List[AlternativeCrop]

class CropRecommendationSave(BaseModel):
    recommendedCrop: str
    successRate: float
    soilCompatibility: float
    growthRate: float
    yieldPotential: float
    fertilizer: FertilizerRecommendation
    alternativeOptions: List[AlternativeCrop]
    soilReadingId: str
    soilData: dict

class SensorData(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    soilPh: float
    temperature: float
    humidity: float
    soilMoisture: float

class StatusUpdate(BaseModel):
    status: str

# Helper function to convert ObjectId to string in nested documents
def convert_objectids(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            elif isinstance(value, dict):
                data[key] = convert_objectids(value)
            elif isinstance(value, list):
                data[key] = [convert_objectids(item) if isinstance(item, dict) else item for item in value]
    return data

# Get latest sensor data from your specific collection structure
@router.get("/sensors/latest")
async def get_latest_sensor_data():
    try:
        db = await get_database()
        
        # Get latest NPK data from esp32-1
        esp32_1 = await db["sensor_readings"].find_one({"_id": "esp32-1"})
        latest_npk = None
        if esp32_1 and "readings" in esp32_1 and len(esp32_1["readings"]) > 0:
            # Get the most recent reading (assuming readings are sorted by timestamp)
            latest_npk = esp32_1["readings"][-1]
        
        # Get latest environmental data from esp32-2
        esp32_2 = await db["sensor_readings"].find_one({"_id": "esp32-2"})
        latest_env = None
        if esp32_2 and "readings" in esp32_2 and len(esp32_2["readings"]) > 0:
            # Get the most recent reading
            latest_env = esp32_2["readings"][-1]
        
        # Combine data
        sensor_data = {
            "nitrogen": latest_npk.get("nitrogen", 0) if latest_npk else 0,
            "phosphorus": latest_npk.get("phosphorus", 0) if latest_npk else 0,
            "potassium": latest_npk.get("potassium", 0) if latest_npk else 0,
            "soilPh": latest_npk.get("soilPh", 0) if latest_npk else 0,
            "temperature": latest_env.get("temperature", 0) if latest_env else 0,
            "humidity": latest_env.get("humidity", 0) if latest_env else 0,
            "soilMoisture": latest_env.get("soilMoisture", 0) if latest_env else 0,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return sensor_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sensors")
async def save_sensor_data(data: SensorData):
    try:
        db = await get_database()
        
        # For your structure, we need to update the specific device documents
        npk_data = {
            "nitrogen": data.nitrogen,
            "phosphorus": data.phosphorus,
            "potassium": data.potassium,
            "soilPh": data.soilPh,
            "device_id": "ESP32-NPKPH",
            "timestamp": datetime.utcnow()
        }
        
        env_data = {
            "temperature": data.temperature,
            "humidity": data.humidity,
            "soilMoisture": data.soilMoisture,
            "device_id": "ESP32-ENV",
            "timestamp": datetime.utcnow()
        }
        
        # Update esp32-1 document with new reading
        await db["sensor_readings"].update_one(
            {"_id": "esp32-1"},
            {"$push": {"readings": npk_data}},
            upsert=True
        )
        
        # Update esp32-2 document with new reading
        await db["sensor_readings"].update_one(
            {"_id": "esp32-2"},
            {"$push": {"readings": env_data}},
            upsert=True
        )
        
        return {"message": "Sensor data saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# REMOVED THE DUPLICATE /stats ENDPOINT THAT WAS HERE

@router.get("/recommendations/filtered")
async def get_filtered_recommendations(
    status: Optional[str] = None,
    min_success_rate: Optional[float] = None,
    max_success_rate: Optional[float] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):
    try:
        db = await get_database()
        collection = db["crop_recommendations"]
        
        # Build query
        query = {}
        
        if status and status != "All":
            query["status"] = status
            
        if min_success_rate is not None:
            query["successRate"] = {"$gte": min_success_rate}
            
        if max_success_rate is not None:
            if "successRate" in query:
                query["successRate"]["$lte"] = max_success_rate
            else:
                query["successRate"] = {"$lte": max_success_rate}
                
        if start_date or end_date:
            query["timestamp"] = {}
            if start_date:
                start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
                query["timestamp"]["$gte"] = start_dt
            if end_date:
                end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                end_dt = end_dt.replace(hour=23, minute=59, second=59)
                query["timestamp"]["$lte"] = end_dt
                
        if search:
            query["recommendedCrop"] = {"$regex": search, "$options": "i"}
        
        # Get total count for pagination
        total = await collection.count_documents(query)
        
        # Get paginated results
        skip = (page - 1) * limit
        cursor = collection.find(query).sort("timestamp", -1).skip(skip).limit(limit)
        
        recommendations = []
        async for doc in cursor:
            timestamp = doc.get("timestamp")
            
            if timestamp:
                try:
                    formatted_date = timestamp.strftime("%b %d, %Y, %I:%M %p")
                except Exception:
                    formatted_date = str(timestamp)
            else:
                formatted_date = "N/A"

            recommendations.append({
                "id": str(doc["_id"]),
                "crop": doc.get("recommendedCrop", ""),
                "successRate": doc.get("successRate", 0.0),
                "status": doc.get("status", "Recommended"),
                "date": formatted_date,
                "alternativeOptions": doc.get("alternativeOptions", []),
                "growthRate": doc.get("growthRate"),
                "soilCompatibility": doc.get("soilCompatibility"),
                "yieldPotential": doc.get("yieldPotential"),
                "fertilizer": doc.get("fertilizer", {})
            })

        return {
            "recommendations": recommendations,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/recommendations/{doc_id}")
async def delete_recommendation(doc_id: str):
    try:
        db = await get_database()
        collection = db["crop_recommendations"]
        
        result = await collection.delete_one({"_id": ObjectId(doc_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Recommendation not found")
            
        return {"message": "Recommendation deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Your existing endpoints with slight modifications for your database structure

@router.post("/recommend", response_model=CropPrediction)
async def recommend_crop(data: CropInput):
    try:
        features_dict = {
            "N (ppm)": data.nitrogen,
            "P (ppm)": data.phosphorus,
            "K (ppm)": data.potassium,
            "Temp (°C)": data.temperature,
            "Humidity (%)": data.humidity,
            "pH": data.soilpH,
            "Soil Moisture (%)": data.soilMoisture
        }

        print("✅ Received crop prediction request with input:")
        print(features_dict)

        result = get_integrated_recommendation(features_dict)

        print("📊 ML Result:", result)

        if "error" in result:
            print("❌ ML Integration Error:", result["error"], result["details"])
            raise HTTPException(
                status_code=500,
                detail=f"{result['error']}: {result['details']}"
            )

        recommendations = result.get("recommendations")
        if not recommendations or len(recommendations) == 0:
            raise HTTPException(
                status_code=500,
                detail="No recommendations generated"
            )

        recommendations = sorted(recommendations, key=lambda x: x['confidence'], reverse=True)
        top_rec = recommendations[0]

        return {
            "recommendedCrop": top_rec.get('crop', 'Unknown'),
            "successRate": round(top_rec.get('confidence', 0.0) * 100, 2),
            "soilCompatibility": top_rec.get('soil_compatibility', 0.0),
            "growthRate": top_rec.get('growth_rate', 0.0),
            "yieldPotential": top_rec.get('yield_potential', 0.0),
            "fertilizer": {
                "type": top_rec['fertilizer'].get('type', ''),
                "name": top_rec['fertilizer'].get('name', ''),
                "base_amount": top_rec['fertilizer'].get('base_amount', 0.0),
                "adjusted_amount": top_rec['fertilizer'].get('adjusted_amount', 0.0),
                "unit": top_rec['fertilizer'].get('unit', '')
            },
            "alternativeOptions": [
                {
                    "crop": rec.get('crop', ''),
                    "confidence": round(rec.get('confidence', 0.0) * 100, 2),
                    "fertilizer": {
                        "type": rec['fertilizer'].get('type', ''),
                        "name": rec['fertilizer'].get('name', ''),
                        "base_amount": rec['fertilizer'].get('base_amount', 0.0),
                        "adjusted_amount": rec['fertilizer'].get('adjusted_amount', 0.0),
                        "unit": rec['fertilizer'].get('unit', '')
                    }
                }
                for rec in recommendations[1:3]
            ]
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save")
async def save_crop_recommendation(data: dict = Body(...)):
    """
    Save crop recommendation with flexible data validation
    """
    try:
        db = await get_database()
        collection = db["crop_recommendations"]
        
        # Prepare the document data
        doc_data = {
            "recommendedCrop": data.get("recommendedCrop", ""),
            "successRate": data.get("successRate", 0.0),
            "soilCompatibility": data.get("soilCompatibility", 0.0),
            "growthRate": data.get("growthRate", 0.0),
            "yieldPotential": data.get("yieldPotential", 0.0),
            "fertilizer": data.get("fertilizer", {}),
            "alternativeOptions": data.get("alternativeOptions", []),
            "soilData": data.get("soilData", {}),
            "status": data.get("status", "Recommended"),
            "timestamp": datetime.utcnow()
        }
        
        # Insert into MongoDB
        result = await collection.insert_one(doc_data)
        
        return {"message": "Crop recommendation saved to MongoDB", "id": str(result.inserted_id)}
        
    except Exception as e:
        print(f"❌ Error saving recommendation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations")
async def get_saved_recommendations():
    try:
        db = await get_database()
        collection = db["crop_recommendations"]
        
        # Get recommendations sorted by timestamp descending
        cursor = collection.find().sort("timestamp", -1)
        recommendations = []
        
        async for doc in cursor:
            timestamp = doc.get("timestamp")
            
            # Handle Firestore timestamp format ({_seconds: xxx, _nanoseconds: yyy})
            formatted_date = "N/A"
            timestamp_iso = ""
            
            if timestamp:
                try:
                    # Handle Firestore timestamp format
                    if isinstance(timestamp, dict) and "_seconds" in timestamp:
                        timestamp_dt = datetime.fromtimestamp(timestamp["_seconds"])
                        formatted_date = timestamp_dt.strftime("%b %d, %Y at %I:%M:%S %p")  # Added time
                        timestamp_iso = timestamp_dt.isoformat()
                    # Handle other timestamp formats
                    elif isinstance(timestamp, datetime):
                        formatted_date = timestamp.strftime("%b %d, %Y at %I:%M:%S %p")  # Added time
                        timestamp_iso = timestamp.isoformat()
                    elif isinstance(timestamp, str):
                        timestamp_dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                        formatted_date = timestamp_dt.strftime("%b %d, %Y at %I:%M:%S %p")  # Added time
                        timestamp_iso = timestamp_dt.isoformat()
                    else:
                        formatted_date = str(timestamp)
                        timestamp_iso = str(timestamp)
                except Exception as e:
                    print(f"Error formatting timestamp: {e}")
                    formatted_date = str(timestamp)
                    timestamp_iso = str(timestamp)

            recommendations.append({
                "id": str(doc["_id"]),
                "recommendedCrop": doc.get("recommendedCrop", ""),
                "crop": doc.get("recommendedCrop", ""),
                "successRate": doc.get("successRate", 0.0),
                "status": doc.get("status", "Recommended"),
                "date": formatted_date,  # This now includes time
                "timestamp": timestamp_iso,
                "alternativeOptions": doc.get("alternativeOptions", []),
                "growthRate": doc.get("growthRate", 0),
                "soilCompatibility": doc.get("soilCompatibility", 0),
                "yieldPotential": doc.get("yieldPotential", 0),
                "fertilizer": doc.get("fertilizer", {})
            })

        return recommendations

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations/stats")
async def get_recommendation_stats():
    try:
        db = await get_database()
        
        # Get stats from your system_stats collection
        stats_doc = await db["system_stats"].find_one({"_id": "crop_recommendation_metrics"})
        
        if not stats_doc:
            # If no stats exist, calculate from crop_recommendations
            total = await db["crop_recommendations"].count_documents({})
            planted = await db["crop_recommendations"].count_documents({"status": "Planted"})
            ongoing = await db["crop_recommendations"].count_documents({"status": "Ongoing"})
            harvested = await db["crop_recommendations"].count_documents({"status": "Harvested"})
            
            success_rate = round((harvested / total * 100) if total > 0 else 0, 1)
            
            current_stats = {
                "total": total,
                "planted": planted,
                "ongoing": ongoing,
                "harvested": harvested,
                "successRate": success_rate
            }
            
            # Create baseline stats document
            baseline_stats = {
                "_id": "crop_recommendation_metrics",
                "total": total,
                "planted": planted,
                "ongoing": ongoing,
                "harvested": harvested,
                "successRate": success_rate,
                "timestamp": datetime.utcnow()
            }
            await db["system_stats"].insert_one(baseline_stats)
            
            return {
                "current": current_stats,
                "baseline": current_stats  # Same as current for first time
            }
        
        # Get current counts from crop_recommendations
        total = await db["crop_recommendations"].count_documents({})
        planted = await db["crop_recommendations"].count_documents({"status": "Planted"})
        ongoing = await db["crop_recommendations"].count_documents({"status": "Ongoing"})
        harvested = await db["crop_recommendations"].count_documents({"status": "Harvested"})
        
        success_rate = round((harvested / total * 100) if total > 0 else 0, 1)
        
        current_stats = {
            "total": total,
            "planted": planted,
            "ongoing": ongoing,
            "harvested": harvested,
            "successRate": success_rate
        }
        
        # Handle timestamp conversion - check if it's a Firestore timestamp object
        stats_timestamp = stats_doc.get("timestamp")
        
        # Convert Firestore timestamp (with seconds/nanoseconds) to datetime
        if isinstance(stats_timestamp, dict) and "seconds" in stats_timestamp:
            stats_timestamp = datetime.fromtimestamp(stats_timestamp["seconds"])
        elif isinstance(stats_timestamp, dict) and "_seconds" in stats_timestamp:
            stats_timestamp = datetime.fromtimestamp(stats_timestamp["_seconds"])
        
        # Update baseline if it's older than 24 hours
        if stats_timestamp and isinstance(stats_timestamp, datetime) and (datetime.utcnow() - stats_timestamp).total_seconds() > 86400:
            updated_stats = {
                "total": total,
                "planted": planted,
                "ongoing": ongoing,
                "harvested": harvested,
                "successRate": success_rate,
                "timestamp": datetime.utcnow()
            }
            await db["system_stats"].update_one(
                {"_id": "crop_recommendation_metrics"},
                {"$set": updated_stats}
            )
            stats_doc = updated_stats
            stats_timestamp = datetime.utcnow()  # Update the timestamp for response
        
        # Prepare baseline stats for response
        baseline_stats = {
            "total": stats_doc.get("total", 0),
            "planted": stats_doc.get("planted", 0),
            "ongoing": stats_doc.get("ongoing", 0),
            "harvested": stats_doc.get("harvested", 0),
            "successRate": stats_doc.get("successRate", 0),
        }
        
        # Add timestamp to baseline stats if it's a datetime object
        if isinstance(stats_timestamp, datetime):
            baseline_stats["timestamp"] = stats_timestamp.isoformat()
        else:
            baseline_stats["timestamp"] = datetime.utcnow().isoformat()
        
        return {
            "current": current_stats,
            "baseline": baseline_stats
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommendations/{doc_id}/status")
async def update_recommendation_status(doc_id: str, status_data: dict = Body(...)):
    """
    Update the status of a crop recommendation.
    Expects: {"status": "Planted"}
    """
    try:
        db = await get_database()
        collection = db["crop_recommendations"]
        
        if "status" not in status_data:
            raise HTTPException(status_code=422, detail="Status field is required")
        
        status_value = status_data["status"]
        print(f"📝 Updating status for document {doc_id} to: {status_value}")
        
        # Try to convert to ObjectId first, if it fails, use the string as-is
        try:
            # Try to convert to ObjectId (for MongoDB-style IDs)
            object_id = ObjectId(doc_id)
            query = {"_id": object_id}
        except:
            # If it's not a valid ObjectId, use the string as-is
            print(f"⚠️  Using string ID (not ObjectId): {doc_id}")
            query = {"_id": doc_id}
        
        # Update the status of the recommendation
        result = await collection.update_one(
            query,
            {"$set": {"status": status_value}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Recommendation not found")
            
        return {"message": "Status updated successfully"}
    except Exception as e:
        print(f"❌ Error updating status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))