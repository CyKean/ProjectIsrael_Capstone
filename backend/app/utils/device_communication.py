import httpx
import os
import logging
from dotenv import load_dotenv
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the path to the .env file relative to this file
current_dir = Path(__file__).resolve().parent
env_path = current_dir.parent.parent / '.env'  # Adjust path based on your structure

# Load environment variables from specific path
if env_path.exists():
    load_dotenv(env_path)
    logger.info(f"Loaded .env file from: {env_path}")
else:
    logger.warning(f".env file not found at: {env_path}")

async def send_to_esp(device_ip: str, endpoint: str, payload: dict):
    """Generic function to send data to ESP devices"""
    try:
        url = f"http://{device_ip}/{endpoint}"
        logger.info(f"Sending to {url} with payload: {payload}")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload)
            logger.info(f"Device response: {response.status_code} {response.text}")
            response.raise_for_status()
            return response.json()
    except httpx.ConnectError:
        error_msg = f"Could not connect to device at {device_ip}"
        logger.error(error_msg)
        raise ConnectionError(error_msg)
    except httpx.TimeoutException:
        error_msg = f"Timeout while connecting to {device_ip}"
        logger.error(error_msg)
        raise TimeoutError(error_msg)
    except httpx.HTTPStatusError as e:
        error_msg = f"Device returned error status: {e.response.status_code} {e.response.text}"
        logger.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Error communicating with device {device_ip}: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

def get_device_ip(device_type: str):
    """Get device IP from environment variables"""
    # Add debug logging to show what's being loaded
    logger.info(f"Environment variables: ESP1_IP={os.getenv('ESP1_IP')}, ESP2_IP={os.getenv('ESP2_IP')}, ESP3_IP={os.getenv('ESP3_IP')}")
    
    ip_mapping = {
        "esp1": os.getenv("ESP1_IP"),
        "esp2": os.getenv("ESP2_IP"),
        "esp3": os.getenv("ESP3_IP")
    }
    
    ip = ip_mapping.get(device_type)
    
    if not ip:
        # Try alternative variable naming
        alt_ip = os.getenv(f"{device_type.upper()}_IP") or os.getenv(f"{device_type.lower()}_ip")
        if alt_ip:
            logger.warning(f"Using alternative variable name for {device_type} IP: {alt_ip}")
            return alt_ip
        
        error_msg = (f"IP address not configured for {device_type}. Check your .env file. "
                     f"Current values: ESP1_IP={os.getenv('ESP1_IP')}, "
                     f"ESP2_IP={os.getenv('ESP2_IP')}, "
                     f"ESP3_IP={os.getenv('ESP3_IP')}")
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    return ip