from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ESP32IPRequest(BaseModel):
    ip: str

class ESP32Config(BaseModel):
    wifi_ssid: Optional[str] = None
    wifi_password: Optional[str] = None
    server_url: Optional[str] = None
    nitrogen_offset: Optional[float] = 0.0
    phosphorus_offset: Optional[float] = 0.0
    potassium_offset: Optional[float] = 0.0
    ph_offset: Optional[float] = 0.0

class SystemInfo(BaseModel):
    version: str
    status: str
    uptime: int
    environment: str
    last_esp32_contact: str