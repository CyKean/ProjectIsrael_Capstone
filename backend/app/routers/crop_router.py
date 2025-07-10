from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from app.ml.integrated_prediction import get_integrated_recommendation
from datetime import datetime
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

router = APIRouter()

load_dotenv()

FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
if not FIREBASE_CREDENTIALS:
    raise ValueError("Firebase credentials not found. Set FIREBASE_CREDENTIALS in .env")

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)

db = firestore.client()

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
async def save_crop_recommendation(data: CropRecommendationSave):
    try:
        doc_data = data.dict()
        doc_data["timestamp"] = datetime.utcnow().isoformat()

        doc_data["alternativeOptions"] = [
            {
                "crop": alt.crop,
                "confidence": alt.confidence,
                "fertilizer": alt.fertilizer.dict()
            } 
            for alt in data.alternativeOptions
        ]

        doc_data["fertilizer"] = data.fertilizer.dict()
        doc_data["status"] = "Recommended"

        doc_data["soilReadingId"] = data.soilReadingId
        doc_data["soilData"] = data.soilData

        db.collection("crop_recommendations").add(doc_data)

        return {"message": "Crop recommendation saved to Firebase"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/recommendations")
async def get_saved_recommendations():
    try:
        docs = db.collection("crop_recommendations") \
                 .order_by("timestamp", direction=firestore.Query.DESCENDING) \
                 .stream()

        recommendations = []
        for doc in docs:
            data = doc.to_dict()
            timestamp = data.get("timestamp")

            if timestamp:
                try:
                    formatted_date = timestamp.strftime("%b %d, %Y, %I:%M %p")
                except Exception:
                    formatted_date = str(timestamp)
            else:
                formatted_date = "N/A"

            recommendations.append({
                "id": doc.id,
                "crop": data.get("recommendedCrop", ""),
                "successRate": data.get("successRate", 0.0),
                "status": data.get("status", "Planted"),
                "date": formatted_date,
                "alternativeOptions": data.get("alternativeOptions", []),
                "growthRate": data.get("growthRate"),
                "soilCompatibility": data.get("soilCompatibility"),
                "yieldPotential": data.get("yieldPotential"),
                "fertilizer": data.get("fertilizer", {})
            })

        return recommendations

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommendations/{doc_id}/status")
async def update_recommendation_status(doc_id: str, status: str):
    try:
        db.collection("crop_recommendations").document(doc_id).update({
            "status": status
        })
        return {"message": "Status updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))