# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# import vonage

# router = APIRouter()

# # Your Vonage API credentials
# VONAGE_API_KEY = '6f176aee'
# VONAGE_API_SECRET = 'P9KyL6hCHMFY7ULT'
# VONAGE_SENDER = 'ProjIsrael'

# # Initialize client (v3.1.0 syntax)
# client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
# sms = vonage.Sms(client)

# class SMSRequest(BaseModel):
#     phone: str
#     message: str

# @router.post("/send-sms")
# def send_sms(payload: SMSRequest):
#     response = sms.send_message({
#         "from": VONAGE_SENDER,
#         "to": payload.phone,
#         "text": payload.message,
#     })

#     if response["messages"][0]["status"] != "0":
#         raise HTTPException(status_code=400, detail=response["messages"][0]["error-text"])
    
#     return {"success": True, "response": response}
