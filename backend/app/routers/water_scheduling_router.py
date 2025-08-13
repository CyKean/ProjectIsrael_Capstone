from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder  # ✅ Add this line
from firebase_admin import firestore
from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import datetime, timedelta
from dependencies import get_esp32_ip
import time
import pytz
import json
import httpx
import traceback

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
def get_schedules_for_esp32():
    try:
        db = firestore.client()
        grace_seconds = 3600
        current_epoch_ms = int((time.time() - grace_seconds) * 1000)

        query = db.collection("watering_schedules") \
            .where("completed", "==", False) \
            .where("scheduledTime", ">", current_epoch_ms) \
            .order_by("scheduledTime")

        schedule_list = []
        for doc in query.stream():
            data = doc.to_dict()
            raw_sched_time = data.get("scheduledTime", 0)
            try:
                if isinstance(raw_sched_time, (int, float)) and raw_sched_time > 0:
                    sched_utc = datetime.utcfromtimestamp(raw_sched_time / 1000) if raw_sched_time > 1_000_000_000_000 else datetime.utcfromtimestamp(raw_sched_time)
                    sched_seconds = int(sched_utc.replace(tzinfo=pytz.utc).timestamp())
                else:
                    raise ValueError("Invalid scheduledTime format")
            except Exception as e:
                print(f"⚠️ Skipping invalid timestamp for doc {doc.id}: {raw_sched_time}")
                continue  # skip this doc and move to next

            sched_seconds = int(sched_utc.replace(tzinfo=pytz.utc).timestamp())

            try:
                flow = float(data.get("waterFlowRate", 0.0))
            except:
                flow = 0.0

            item = {
                "id": doc.id,
                "dateTime": data.get("dateTime", ""),
                "duration": int(data.get("duration", 0)),
                "mode": data.get("mode", "one-time"),
                "days": data.get("days", [False]*7),
                "interval": data.get("interval", {"unit": "day", "value": 1}),
                "scheduledTime": sched_seconds,
                "skipIfRain": data.get("skipIfRain", False),
                "notifyWatering": data.get("notifyWatering", False),
                "waterFlowRate": flow,
                "completed": data.get("completed", False),
                "action": data.get("action", "add")
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
async def handle_schedule_operation(request: Request,esp_ip: str = Depends(get_esp32_ip)):
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
            print(f"🗑️ Deleting from Firestore: watering_schedules → {schedule.id}")
            db = firestore.client()
            db.collection("watering_schedules").document(schedule.id).delete()

            # ✅ Notify ESP32 to delete the same ID from its memory
            esp_url = "http://{esp_ip}/watering-schedule"  # <-- adjust if needed
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

        # Send to ESP32
        esp_url = "http://{esp_ip}/watering-schedule"
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
def mark_schedule_complete():
    try:
        db = firestore.client()
        schedules = db.collection("watering_schedules").order_by("scheduledTime").stream()

        for doc in schedules:
            data = doc.to_dict()
            doc_ref = db.collection("watering_schedules").document(doc.id)

            scheduled_time = data.get("scheduledTime", 0)
            scheduled_sec = int(scheduled_time / 1000) if scheduled_time > 1_000_000_000_000 else scheduled_time

            if not data.get("completed", False) and scheduled_sec <= int(time.time()):
                if data.get("mode") in ["one-time", "calendar-day"]:
                    doc_ref.update({"completed": True})
                    print(f"✅ Marked complete: {doc.id}")
                    return {"status": "completed", "id": doc.id}
                else:
                    print(f"🔁 Skipped recurring: {doc.id}")
                    return {"status": "recurring", "id": doc.id}

        return {"status": "no-action"}

    except Exception as e:
        print("❌ Failed to mark schedule complete:", str(e))
        return {"error": str(e)}

# @router.post("/api/watering-log")
# async def log_watering(req: Request):
#     try:
#         body = await req.json()
#         log = WateringLog(**body)
#         db = firestore.client()
#         db.collection("watering_logs").add(log.dict())
#         print(f"📝 Watering logged: {log.schedule_id}")
#         return {"status": "logged"}

#     except Exception as e:
#         print("❌ Failed to log watering:", str(e))
#         return {"error": str(e)}
    
@router.post("/api/schedule-status")
async def update_schedule_status(request: Request):
    try:
        body = await request.json()
        schedule_id = body.get("id")
        completed_status = body.get("status", False)

        if not schedule_id:
            raise HTTPException(status_code=400, detail="Missing schedule ID")

        db = firestore.client()
        doc_ref = db.collection("watering_schedules").document(schedule_id)
        doc_ref.update({"completed": completed_status})

        print(f"✅ Schedule {schedule_id} marked as completed: {completed_status}")
        return {"status": "updated", "id": schedule_id, "completed": completed_status}

    except Exception as e:
        print("❌ Failed to update schedule status:", str(e))
        return {"error": str(e)}
