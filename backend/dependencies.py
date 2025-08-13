from app.services.esp32_ip_manager import ip_manager
from fastapi import Depends

def get_esp32_ip():
    return ip_manager.get_ip()