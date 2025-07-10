# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# import os
# import vonage
# from dotenv import load_dotenv

# load_dotenv()

# router = APIRouter(prefix="/api/otp", tags=["OTP"])

# VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
# VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")
# VONAGE_BRAND_NAME = os.getenv("VONAGE_BRAND_NAME")

# client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
# sms = vonage.Sms(client)

# class OTPRequest(BaseModel):
#     number: str
#     message: str

# @router.post("/send")
# def send_otp(payload: OTPRequest):
#     try:
#         responseData = sms.send_message({
#             "from": VONAGE_BRAND_NAME,
#             "to": payload.number,
#             "text": payload.message,
#         })

#         if responseData["messages"][0]["status"] == "0":
#             return {"success": True, "message": "OTP sent successfully"}
#         else:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Vonage Error: {responseData['messages'][0]['error-text']}"
#             )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
