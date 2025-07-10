from app.utils.device_communication import send_to_esp, get_device_ip
from app.models.config_models import ESP2Config

async def configure_esp2(config: ESP2Config):
    device_ip = get_device_ip("esp2")
    payload = {
        "wifi": {
            "ssid": config.wifiSSID,
            "password": config.wifiPassword
        },
        "api_url": config.apiURL,
        "temp_offset": config.tempOffset,
        "humidity_offset": config.humidityOffset,
        "watering_threshold": config.wateringThreshold,
        "soil_calibration": {
            "air_value": config.airValue,
            "water_value": config.waterValue
        }
    }
    return await send_to_esp(device_ip, "config", payload)