from pydantic import BaseModel, Field

class CropInput(BaseModel):
    N: float = Field(..., description="Ratio of Nitrogen content in soil")
    P: float = Field(..., description="Ratio of Phosphorous content in soil")
    K: float = Field(..., description="Ratio of Potassium content in soil")
    temperature: float = Field(..., description="Temperature in celsius")
    humidity: float = Field(..., description="Relative humidity in %")
    ph: float = Field(..., description="pH value of the soil")
    rainfall: float = Field(..., description="Rainfall in mm")

class CropPrediction(BaseModel):
    crop: str
    probability: float
