from app.utils.device_communication import send_to_esp, get_device_ip
from app.models.config_models import ESP3Config

async def configure_esp3(config: ESP3Config):
    device_ip = get_device_ip("esp3")
    payload = {
        "wifi": {
            "ssid": config.wifiSSID,
            "password": config.wifiPassword
        },
        "api_url": config.apiURL,
        "tank_config": {
            "height": config.tankHeight,
            "alert_level": config.alertLevel
        },
        "sensor_calibration": {
            "full_distance": config.fullDistance,
            "empty_distance": config.emptyDistance
        }
    }
    return await send_to_esp(device_ip, "config", payload)