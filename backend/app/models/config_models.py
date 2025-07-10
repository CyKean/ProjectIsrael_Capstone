from pydantic import BaseModel

class ESP1Config(BaseModel):
    wifiSSID: str
    wifiPassword: str
    serverURL: str
    nitrogenOffset: float
    phosphorusOffset: float
    potassiumOffset: float
    phOffset: float

class ESP2Config(BaseModel):
    wifiSSID: str
    wifiPassword: str
    apiURL: str
    tempOffset: float
    humidityOffset: float
    wateringThreshold: int
    airValue: int
    waterValue: int

class ESP3Config(BaseModel):
    wifiSSID: str
    wifiPassword: str
    apiURL: str
    tankHeight: float
    alertLevel: int
    fullDistance: float
    emptyDistance: float