from app.utils.device_communication import send_to_esp, get_device_ip
from app.models.config_models import ESP1Config

async def configure_esp1(config: ESP1Config):
    device_ip = get_device_ip("esp1")
    payload = {
        "wifi": {
            "ssid": config.wifiSSID,
            "password": config.wifiPassword
        },
        "server_url": config.serverURL,
        "sensor_offsets": {
            "nitrogen": config.nitrogenOffset,
            "phosphorus": config.phosphorusOffset,
            "potassium": config.potassiumOffset,
            "ph": config.phOffset
        }
    }
    return await send_to_esp(device_ip, "config", payload)