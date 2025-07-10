import firebase_admin
from firebase_admin import credentials, firestore
import socket
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load Firebase credentials dynamically
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")

# Initialize Firebase only if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_local_ip():
    """Returns the Wi-Fi/local network IP address (e.g., 192.168.x.x)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable, just used to determine local IP
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    finally:
        s.close()
    return ip_address

def save_backend_ip():
    ip_address = get_local_ip()
    print(f"🔌 Backend Wi-Fi IP: {ip_address}")

    db.collection("network").document("backend").set({
        "ip_address": ip_address
    })

save_backend_ip()
