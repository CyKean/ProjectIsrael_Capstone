# import json
# from pathlib import Path
# from fastapi import HTTPException
# from typing import Optional

# class ESP32IPManager:
#     _instance = None
#     _storage_path = Path("esp32_ip_store.json")
    
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(ESP32IPManager, cls).__new__(cls)
#             cls._instance._initialize()
#         return cls._instance
    
#     def _initialize(self):
#         self._ip: Optional[str] = None
#         self._load_ip()
    
#     def _load_ip(self):
#         try:
#             if self._storage_path.exists():
#                 with open(self._storage_path) as f:
#                     data = json.load(f)
#                     self._ip = data.get("ip", "192.168.1.14")
#             else:
#                 self._ip = "192.168.1.14"
#                 self._save_ip()  # Create file with default
#         except Exception as e:
#             print(f"Error loading IP: {e}")
#             self._ip = "192.168.1.14"
    
#     def _save_ip(self):
#         try:
#             with open(self._storage_path, "w") as f:
#                 json.dump({"ip": self._ip}, f)
#         except Exception as e:
#             print(f"Error saving IP: {e}")
    
#     def get_ip(self) -> str:
#         return self._ip or "192.168.1.14"
    
#     def set_ip(self, ip: str):
#         if not self.is_valid_ip(ip):
#             raise ValueError("Invalid IP address format")
#         self._ip = ip
#         self._save_ip()
    
#     @staticmethod
#     def is_valid_ip(ip: str) -> bool:
#         parts = ip.split('.')
#         if len(parts) != 4:
#             return False
#         try:
#             return all(0 <= int(part) <= 255 for part in parts)
#         except ValueError:
#             return False

# # Global instance
# ip_manager = ESP32IPManager()

import json
from pathlib import Path
from fastapi import HTTPException
from typing import Optional
import os

class ESP32IPManager:
    _instance = None
    # Go up one level from services directory to main directory
    _storage_path = Path(__file__).parent.parent / "esp32_ip_store.json"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ESP32IPManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self._ip: Optional[str] = None
        self._last_contact: Optional[str] = None
        self._load_ip()
    
    def _load_ip(self):
        try:
            if self._storage_path.exists():
                with open(self._storage_path) as f:
                    data = json.load(f)
                    self._ip = data.get("ip", "192.168.1.14")
                    self._last_contact = data.get("last_contact")
            else:
                self._ip = "192.168.1.14"
                self._save_ip()  # Create file with default
        except Exception as e:
            print(f"Error loading IP: {e}")
            self._ip = "192.168.1.14"
    
    def _save_ip(self):
        try:
            with open(self._storage_path, "w") as f:
                json.dump({
                    "ip": self._ip,
                    "last_contact": self._last_contact
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving IP: {e}")
            raise HTTPException(
                status_code=500,
                detail="Could not save IP address"
            )
    
    def get_ip(self) -> str:
        return self._ip or "192.168.1.14"
    
    def get_last_contact(self) -> Optional[str]:
        return self._last_contact
    
    def set_ip(self, ip: str):
        if not self.is_valid_ip(ip):
            raise ValueError("Invalid IP address format")
        self._ip = ip
        self._last_contact = datetime.now().isoformat()
        self._save_ip()
    
    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(part) <= 255 for part in parts)
        except ValueError:
            return False

# Global instance
ip_manager = ESP32IPManager()