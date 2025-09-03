from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import datetime, timedelta
from dependencies import get_esp32_ip
import time
import pytz
import json
import httpx
import traceback
from app.services.database import get_database
from bson import ObjectId

router = APIRouter()

# === Models ===

class Interval(BaseModel):
    value: int
    unit: str  # days, weeks, hours

class DeleteSchedule(BaseModel):
    action: str
    id: str

class Schedule(BaseModel):
    id: Optional[str] = None
    dateTime: Optional[str] = None
    duration: Optional[int] = None
    mode: Optional[str] = None
    days: Optional[List[bool]] = None
    skipIfRain: Optional[bool] = None
    notifyWatering: Optional[bool] = None
    waterFlowRate: Optional[Union[float, str]] = None
    interval: Optional[Interval] = None
    scheduledTime: Optional[int] = None
    completed: Optional[bool] = None
    action: str

class WateringLog(BaseModel):
    schedule_id: str
    executed_at: int
    duration: int
    device_id: str
    status: str

# === Utilities ===

def compute_next_epoch(schedule: Schedule) -> int:
    if not schedule.dateTime:
        print("⚠️ No dateTime provided in schedule. Skipping epoch computation.")
        return int(time.time()) + 3600  # fallback time

    now = datetime.now()
    try:
        selected = datetime.strptime(schedule.dateTime, "%a, %b %d, %I:%M %p")
    except ValueError:
        try:
            selected = datetime.strptime(schedule.dateTime, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            print("❌ Failed to parse dateTime")
            return 0

    target_time = selected.time()
    day_of_month = selected.day

    if schedule.mode == "calendar-day":
        year, month = now.year, now.month
        for _ in range(24):
            try:
                candidate = datetime(year, month, day_of_month, target_time.hour, target_time.minute)
                if candidate > now:
                    return int(candidate.timestamp())
            except ValueError:
                pass
            month += 1
            if month > 12:
                month = 1
                year += 1
        return 0

    if schedule.mode == "one-time":
        if schedule.scheduledTime:
            return schedule.scheduledTime
        manila = pytz.timezone("Asia/Manila")
        selected_local = manila.localize(selected)
        selected_utc = selected_local.astimezone(pytz.utc)
        return int(selected_utc.timestamp())

    if schedule.mode == "daily":
        dt = datetime.combine(now.date(), target_time)
        if dt <= now:
            dt += timedelta(days=1)
        return int(dt.timestamp())

    if schedule.mode == "weekly":
        today = now.weekday()
        for i in range(7):
            day_index = (today + i) % 7
            if schedule.days and schedule.days[day_index]:
                dt = datetime.combine(now.date() + timedelta(days=i), target_time)
                if dt > now:
                    return int(dt.timestamp())
        return int(time.time()) + 86400

    if schedule.mode == "custom" and schedule.interval:
        dt = datetime.combine(now.date(), target_time)
        interval_days = schedule.interval.value if schedule.interval.unit == "days" else 1
        while dt <= now:
            dt += timedelta(days=interval_days)
        return int(dt.timestamp())

    return 0

# === Routes ===

@router.get("/api/watering-schedule")
async def get_schedules_for_esp32():
    try:
        db = await get_database()
        collection = db["watering_schedules"]
        
        grace_seconds = 3600
        current_epoch_ms = int((time.time() - grace_seconds) * 1000)

        # Build query for incomplete schedules with future scheduledTime
        query_filter = {
            "completed": False,
            "scheduledTime": {"$gt": current_epoch_ms}
        }

        cursor = collection.find(query_filter).sort("scheduledTime", 1)
        schedule_list = []
        
        async for doc in cursor:
            raw_sched_time = doc.get("scheduledTime", 0)
            try:
                if isinstance(raw_sched_time, (int, float)) and raw_sched_time > 0:
                    # Handle both milliseconds and seconds timestamps
                    if raw_sched_time > 1_000_000_000_000:  # Likely milliseconds
                        sched_utc = datetime.utcfromtimestamp(raw_sched_time / 1000)
                    else:  # Likely seconds
                        sched_utc = datetime.utcfromtimestamp(raw_sched_time)
                    sched_seconds = int(sched_utc.replace(tzinfo=pytz.utc).timestamp())
                else:
                    raise ValueError("Invalid scheduledTime format")
            except Exception as e:
                print(f"⚠️ Skipping invalid timestamp for doc {doc['_id']}: {raw_sched_time}")
                continue  # skip this doc and move to next

            try:
                flow = float(doc.get("waterFlowRate", 0.0))
            except:
                flow = 0.0

            item = {
                "id": str(doc["_id"]),
                "dateTime": doc.get("dateTime", ""),
                "duration": int(doc.get("duration", 0)),
                "mode": doc.get("mode", "one-time"),
                "days": doc.get("days", [False]*7),
                "interval": doc.get("interval", {"unit": "day", "value": 1}),
                "scheduledTime": sched_seconds,
                "skipIfRain": doc.get("skipIfRain", False),
                "notifyWatering": doc.get("notifyWatering", False),
                "waterFlowRate": flow,
                "completed": doc.get("completed", False),
                "action": doc.get("action", "add")
            }

            if item["mode"] == "custom":
                item["custom_interval"] = item["interval"]

            schedule_list.append(item)

        print("📤 Sending schedules to ESP32 (UTC):")
        print(json.dumps(schedule_list, indent=2))

        return JSONResponse(content={
            "schedules": schedule_list,
            "currentTime": int(time.time())
        })

    except Exception as e:
        print("❌ Error in GET /api/watering-schedule:", str(e))
        traceback.print_exc()
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "schedules": [],
            "currentTime": int(time.time())
        })
    
@router.post("/api/watering-schedule")
async def handle_schedule_operation(request: Request, esp_ip: str = Depends(get_esp32_ip)):
    try:
        body = await request.json()

        # Fix common typos in incoming data
        if "skiptisan" in body:
            body["skipIfRain"] = body.pop("skiptisan")
        if "notifyMatering" in body:
            body["notifyWatering"] = body.pop("notifyMatering")
        if "waterflosette" in body:
            body["waterFlowRate"] = body.pop("waterflosette")

        # Validate and convert scheduleTime
        if "scheduleTime" in body and isinstance(body["scheduleTime"], str):
            try:
                if ":" in body["scheduleTime"]:
                    parts = body["scheduleTime"].split(":")
                    if len(parts) == 3:
                        hours, mins, secs = map(int, parts)
                        body["scheduledTime"] = int(datetime.now().replace(
                            hour=hours, minute=mins, second=secs
                        ).timestamp())
                else:
                    body["scheduledTime"] = int(body["scheduleTime"])
                del body["scheduleTime"]
            except:
                body["scheduledTime"] = int(time.time()) + 3600  # Fallback: 1hr later

        action = body.get("action", "add")
        schedule = Schedule(**body)

        print(f"📥 Received schedule to {action.upper()}:")
        print(json.dumps(schedule.dict(), indent=2))

        # 🔒 Handle DELETE early to skip unnecessary logic
        if action == "delete":
            print(f"🗑️ Deleting from MongoDB: watering_schedules → {schedule.id}")
            db = await get_database()
            collection = db["watering_schedules"]
            
            # Delete the schedule
            result = await collection.delete_one({"_id": ObjectId(schedule.id)})
            
            if result.deleted_count == 0:
                print(f"⚠️ Schedule {schedule.id} not found in MongoDB")

            # ✅ Notify ESP32 to delete the same ID from its memory
            esp_url = f"http://{esp_ip}/watering-schedule"  # <-- adjust if needed
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(esp_url, json={
                        "id": schedule.id,
                        "action": "delete"
                    })
                    print("📤 Sent delete to ESP32.")
                    print("🔁 ESP32 response:", response.text)
            except Exception as e:
                print("⚠️ Failed to notify ESP32:", str(e))

            return JSONResponse(content={"status": "deleted", "id": schedule.id})

        # ✅ Water FlowRate Handling with Mapping
        flow_map = {
            "low": 0.5,
            "medium": 1.0,
            "high": 1.5
        }

        raw_flow = schedule.waterFlowRate
        if isinstance(raw_flow, str):
            flow = flow_map.get(raw_flow.lower(), 1.0)
        else:
            try:
                flow = float(raw_flow)
            except:
                flow = 1.0

        # ✅ Schedule time fallback if not set
        computed_epoch = compute_next_epoch(schedule) if not schedule.scheduledTime else schedule.scheduledTime

        # Prepare payload for ESP32
        esp_payload = {
            "id": schedule.id,
            "dateTime": schedule.dateTime,
            "duration": schedule.duration,
            "mode": schedule.mode,
            "days": schedule.days or [],
            "skipIfRain": schedule.skipIfRain,
            "notifyWatering": schedule.notifyWatering,
            "waterFlowRate": flow,
            "scheduledTime": computed_epoch,
            "completed": schedule.completed,
            "action": action
        }

        # Save to MongoDB if adding/updating
        if action in ["add", "update"]:
            db = await get_database()
            collection = db["watering_schedules"]
            
            schedule_data = esp_payload.copy()
            if schedule.id:
                # Update existing schedule
                schedule_data["_id"] = ObjectId(schedule.id)
                await collection.replace_one({"_id": ObjectId(schedule.id)}, schedule_data, upsert=True)
            else:
                # Insert new schedule
                result = await collection.insert_one(schedule_data)
                esp_payload["id"] = str(result.inserted_id)

        # Send to ESP32
        esp_url = f"http://{esp_ip}/watering-schedule"
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    esp_url,
                    json=jsonable_encoder(esp_payload, exclude_none=True),
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                return JSONResponse(content={
                    "status": "success",
                    "esp32_response": response.json()
                })
            except httpx.RequestError as e:
                print(f"🚨 ESP32 connection failed: {str(e)}")
                return JSONResponse(
                    status_code=502,
                    content={"error": "ESP32 unavailable", "details": str(e)}
                )

    except Exception as e:
        print(f"❌ Schedule processing failed: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/watering-schedule/complete")
async def mark_schedule_complete():
    try:
        db = await get_database()
        collection = db["watering_schedules"]
        
        cursor = collection.find().sort("scheduledTime", 1)
        current_time = int(time.time())
        
        async for doc in cursor:
            data = doc
            scheduled_time = data.get("scheduledTime", 0)
            
            # Handle both milliseconds and seconds timestamps
            if scheduled_time > 1_000_000_000_000:  # Likely milliseconds
                scheduled_sec = int(scheduled_time / 1000)
            else:  # Likely seconds
                scheduled_sec = scheduled_time

            if not data.get("completed", False) and scheduled_sec <= current_time:
                if data.get("mode") in ["one-time", "calendar-day"]:
                    await collection.update_one(
                        {"_id": doc["_id"]},
                        {"$set": {"completed": True}}
                    )
                    print(f"✅ Marked complete: {doc['_id']}")
                    return {"status": "completed", "id": str(doc["_id"])}
                else:
                    print(f"🔁 Skipped recurring: {doc['_id']}")
                    return {"status": "recurring", "id": str(doc["_id"])}

        return {"status": "no-action"}

    except Exception as e:
        print("❌ Failed to mark schedule complete:", str(e))
        return {"error": str(e)}

@router.post("/api/schedule-status")
async def update_schedule_status(request: Request):
    try:
        body = await request.json()
        schedule_id = body.get("id")
        completed_status = body.get("status", False)

        if not schedule_id:
            raise HTTPException(status_code=400, detail="Missing schedule ID")

        db = await get_database()
        collection = db["watering_schedules"]
        
        await collection.update_one(
            {"_id": ObjectId(schedule_id)},
            {"$set": {"completed": completed_status}}
        )

        print(f"✅ Schedule {schedule_id} marked as completed: {completed_status}")
        return {"status": "updated", "id": schedule_id, "completed": completed_status}

    except Exception as e:
        print("❌ Failed to update schedule status:", str(e))
        return {"error": str(e)}