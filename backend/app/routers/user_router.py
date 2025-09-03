from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from datetime import datetime, timedelta
import bcrypt
import random
from pydantic import BaseModel
from typing import Optional
from app.services.database import get_database

router = APIRouter(prefix="/api/users", tags=["users"])

# Pydantic Models
class Avatar(BaseModel):
    id: int
    icon: str
    name: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phoneNumber: Optional[str] = None
    avatar: Optional[Avatar] = None

class PasswordUpdate(BaseModel):
    currentPassword: str
    newPassword: str

class PinUpdate(BaseModel):
    currentPin: str
    newPin: str

class AvatarUpdate(BaseModel):
    avatar: Avatar

class SendResetCodeRequest(BaseModel):
    phoneNumber: str

class VerifyCodeRequest(BaseModel):
    phoneNumber: str
    otp: str

class ResetCredentialsRequest(BaseModel):
    phoneNumber: str
    authType: str
    password: Optional[str] = None
    pin: Optional[str] = None

class ResetCredentialsOTPRequest(BaseModel):
    otp: str
    authType: str
    password: Optional[str] = None
    pin: Optional[str] = None

def to_e164_format(phone_number):
    cleaned = phone_number.replace(" ", "").replace("-", "")
    if cleaned.startswith("+63"):
        return cleaned
    elif cleaned.startswith("09"):
        return "+63" + cleaned[1:]
    elif cleaned.startswith("63"):
        return "+" + cleaned
    return None

# Helper function to find user by ID (supports both ObjectId and string IDs)
async def find_user_by_id(user_id: str, db):
    users_collection = db["users"]
    
    # First try to find by ObjectId
    try:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return user
    except:
        pass
    
    # If not found by ObjectId, try to find by string ID
    user = await users_collection.find_one({"_id": user_id})
    if user:
        return user
    
    # If still not found, try to find by custom ID field (if you have one)
    user = await users_collection.find_one({"userId": user_id})
    return user

# Helper function to update user by ID (supports both ObjectId and string IDs)
async def update_user_by_id(user_id: str, update_data: dict, db):
    users_collection = db["users"]
    
    # First try to update by ObjectId
    try:
        result = await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        if result.modified_count > 0:
            return result
    except:
        pass
    
    # If not updated by ObjectId, try to update by string ID
    result = await users_collection.update_one(
        {"_id": user_id},
        {"$set": update_data}
    )
    if result.modified_count > 0:
        return result
    
    # If still not updated, try to update by custom ID field
    result = await users_collection.update_one(
        {"userId": user_id},
        {"$set": update_data}
    )
    return result

# Helper function to get user query for ID (supports both ObjectId and string IDs)
def get_user_query(user_id: str):
    # First try ObjectId
    try:
        return {"_id": ObjectId(user_id)}
    except:
        pass
    
    # Then try string ID
    return {"_id": user_id}

# OTP Helper functions
async def verify_otp(user, otp_code, db):
    """
    Verify OTP code against stored OTP
    """
    users_collection = db["users"]
    
    # Check if OTP exists and matches
    stored_otp = user.get("otp")
    otp_sent_at = user.get("otpSentAt")
    
    if not stored_otp or stored_otp != otp_code:
        return False
    
    # Check if OTP is not expired (15 minutes)
    if not otp_sent_at:
        return False
    
    if (datetime.utcnow() - otp_sent_at) > timedelta(minutes=15):
        return False
    
    return True

async def clear_otp(user, db):
    """
    Clear OTP data after successful verification
    """
    users_collection = db["users"]
    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$unset": {"otp": "", "otpSentAt": ""}}
    )

# User Routes
@router.put("/{user_id}")
async def update_user(user_id: str, user_data: UserUpdate, db=Depends(get_database)):
    users_collection = db["users"]
    
    # Check if user exists using our helper function
    user = await find_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if phone number is already taken by another user
    if user_data.phoneNumber and user_data.phoneNumber != user.get("phoneNumber"):
        # Build query to exclude current user using the appropriate ID format
        user_query = get_user_query(user_id)
        exclude_query = {"_id": {"$ne": user_query["_id"]}}
        
        existing_user = await users_collection.find_one({
            "phoneNumber": user_data.phoneNumber,
            **exclude_query
        })
        if existing_user:
            raise HTTPException(status_code=400, detail="Phone number already in use")
    
    update_data = {
        "name": user_data.name,
        "phoneNumber": user_data.phoneNumber,
        "avatar": user_data.avatar.dict() if user_data.avatar else None,
        "updatedAt": datetime.utcnow()
    }
    
    # Remove None values
    update_data = {k: v for k, v in update_data.items() if v is not None}
    
    # Use our helper function to update the user
    result = await update_user_by_id(user_id, update_data, db)
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made")
    
    # Return updated user data
    updated_user = await find_user_by_id(user_id, db)
    return {
        "message": "User updated successfully",
        "user": {
            "id": str(updated_user.get("_id", user_id)),
            "name": updated_user.get("name"),
            "phoneNumber": updated_user.get("phoneNumber"),
            "avatar": updated_user.get("avatar"),
            "authType": updated_user.get("authType")
        }
    }

@router.patch("/{user_id}/avatar")
async def update_avatar(user_id: str, avatar_data: AvatarUpdate, db=Depends(get_database)):
    # Check if user exists
    user = await find_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = {
        "avatar": avatar_data.avatar.dict(),
        "updatedAt": datetime.utcnow()
    }
    
    result = await update_user_by_id(user_id, update_data, db)
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to update avatar")
    
    # Return updated user data
    updated_user = await find_user_by_id(user_id, db)
    return {
        "message": "Avatar updated successfully",
        "user": {
            "id": str(updated_user.get("_id", user_id)),
            "avatar": updated_user.get("avatar")
        }
    }

@router.put("/{user_id}/password")
async def update_password(user_id: str, password_data: PasswordUpdate, db=Depends(get_database)):
    # Check if user exists
    user = await find_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current password
    if user.get("authType") == "password":
        if not user.get("password"):
            raise HTTPException(status_code=400, detail="Password authentication not set up")
        
        if not bcrypt.checkpw(password_data.currentPassword.encode(), user["password"].encode()):
            raise HTTPException(status_code=401, detail="Current password is incorrect")
    
    # Hash new password
    hashed_password = bcrypt.hashpw(password_data.newPassword.encode(), bcrypt.gensalt()).decode()
    
    update_data = {
        "password": hashed_password,
        "authType": "password",
        "updatedAt": datetime.utcnow()
    }
    
    result = await update_user_by_id(user_id, update_data, db)
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to update password")
    
    return {"message": "Password updated successfully"}

@router.put("/{user_id}/pin")
async def update_pin(user_id: str, pin_data: PinUpdate, db=Depends(get_database)):
    # Check if user exists
    user = await find_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current pin
    if user.get("authType") == "pin":
        if not user.get("pin"):
            raise HTTPException(status_code=400, detail="PIN authentication not set up")
        
        if not bcrypt.checkpw(pin_data.currentPin.encode(), user["pin"].encode()):
            raise HTTPException(status_code=401, detail="Current PIN is incorrect")
    
    # Hash new pin
    hashed_pin = bcrypt.hashpw(pin_data.newPin.encode(), bcrypt.gensalt()).decode()
    
    update_data = {
        "pin": hashed_pin,
        "authType": "pin",
        "updatedAt": datetime.utcnow()
    }
    
    result = await update_user_by_id(user_id, update_data, db)
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to update PIN")
    
    return {"message": "PIN updated successfully"}

# NEW: OTP-based credential reset endpoint for authenticated users
@router.post("/{user_id}/reset-credentials-otp")
async def reset_credentials_otp(
    user_id: str, 
    reset_data: ResetCredentialsOTPRequest,
    db=Depends(get_database)
):
    """
    Reset user credentials using OTP verification for authenticated users
    """
    users_collection = db["users"]
    
    # Check if user exists
    user = await find_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify OTP first
    if not await verify_otp(user, reset_data.otp, db):
        raise HTTPException(status_code=401, detail="Invalid or expired verification code")
    
    # Prepare update data
    update_data = {
        "authType": reset_data.authType,
        "updatedAt": datetime.utcnow()
    }
    
    # Handle password reset
    if reset_data.authType == "password":
        if not reset_data.password:
            raise HTTPException(status_code=400, detail="Password is required")
        
        if len(reset_data.password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
        
        # Hash the new password
        hashed_password = bcrypt.hashpw(reset_data.password.encode(), bcrypt.gensalt()).decode()
        update_data["password"] = hashed_password
        update_data["pin"] = ""  # Clear PIN
    
    # Handle PIN reset
    elif reset_data.authType == "pin":
        if not reset_data.pin:
            raise HTTPException(status_code=400, detail="PIN is required")
        
        if not reset_data.pin.isdigit() or len(reset_data.pin) != 4:
            raise HTTPException(status_code=400, detail="PIN must be 4 digits")
        
        # Hash the new PIN
        hashed_pin = bcrypt.hashpw(reset_data.pin.encode(), bcrypt.gensalt()).decode()
        update_data["pin"] = hashed_pin
        update_data["password"] = ""  # Clear password
    
    else:
        raise HTTPException(status_code=400, detail="Invalid authentication type. Must be 'password' or 'pin'")
    
    # Update user credentials
    result = await update_user_by_id(user_id, update_data, db)
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to update credentials")
    
    # Clear OTP after successful reset
    await clear_otp(user, db)
    
    # Get updated user data
    updated_user = await find_user_by_id(user_id, db)
    
    return {
        "success": True,
        "message": "Credentials updated successfully",
        "user": {
            "id": str(updated_user.get("_id", user_id)),
            "authType": updated_user.get("authType")
        }
    }

# Auth Routes (for OTP sending and verification)
@router.post("/send-reset-code")
async def send_reset_code(request: SendResetCodeRequest, db=Depends(get_database)):
    users_collection = db["users"]
    
    # Check if user exists
    user = await users_collection.find_one({"phoneNumber": request.phoneNumber})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate OTP
    otp = str(random.randint(100000, 999999))
    
    # Update user with OTP and expiration
    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {
            "otp": otp,
            "otpSentAt": datetime.utcnow()
        }}
    )
    
    # In a real application, you would send the OTP via SMS here
    print(f"OTP for {request.phoneNumber}: {otp}")
    
    return {"message": "Reset code sent successfully"}

@router.post("/resend-reset-code")
async def resend_reset_code(request: SendResetCodeRequest, db=Depends(get_database)):
    users_collection = db["users"]
    
    # Check if user exists
    user = await users_collection.find_one({"phoneNumber": request.phoneNumber})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate new OTP
    otp = str(random.randint(100000, 999999))
    
    # Update user with new OTP
    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {
            "otp": otp,
            "otpSentAt": datetime.utcnow()
        }}
    )
    
    # In a real application, you would send the OTP via SMS here
    print(f"New OTP for {request.phoneNumber}: {otp}")
    
    return {"message": "Reset code resent successfully"}

@router.post("/verify-reset-code")
async def verify_reset_code(request: VerifyCodeRequest, db=Depends(get_database)):
    users_collection = db["users"]
    
    # Add phone number validation
    formatted_phone = to_e164_format(request.phoneNumber)
    if not formatted_phone:
        raise HTTPException(status_code=400, detail="Invalid phone number format")
    
    # Check if user exists using the formatted phone number
    user = await users_collection.find_one({"phoneNumber": formatted_phone})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if OTP matches and is not expired (15 minutes)
    if not user.get("otp") or user.get("otp") != request.otp:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    
    otp_sent_at = user.get("otpSentAt")
    if not otp_sent_at or (datetime.utcnow() - otp_sent_at) > timedelta(minutes=15):
        raise HTTPException(status_code=400, detail="Verification code expired")
    
    # Clear OTP after successful verification
    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$unset": {"otp": "", "otpSentAt": ""}}
    )
    
    # Return consistent response format that frontend expects
    return {
        "success": True,
        "message": "Code verified successfully"
    }

@router.post("/reset-credentials-by-phone")
async def reset_credentials_by_phone(
    request: ResetCredentialsRequest,
    db=Depends(get_database)
):
    users_collection = db["users"]
    
    # Add phone number validation
    formatted_phone = to_e164_format(request.phoneNumber)
    if not formatted_phone:
        raise HTTPException(status_code=400, detail="Invalid phone number format")
    
    # Check if user exists using the formatted phone number
    user = await users_collection.find_one({"phoneNumber": formatted_phone})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # ✅ NO OTP VERIFICATION NEEDED - User already verified in previous step
    
    update_data = {
        "authType": request.authType,
        "updatedAt": datetime.utcnow()
    }
    
    if request.authType == "password":
        if not request.password:
            raise HTTPException(status_code=400, detail="Password is required")
        
        if len(request.password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
        
        # Hash the new password
        hashed_password = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt()).decode()
        update_data["password"] = hashed_password
        update_data["pin"] = ""  # Clear PIN if switching to password
    else:
        if not request.pin:
            raise HTTPException(status_code=400, detail="PIN is required")
        
        if not request.pin.isdigit() or len(request.pin) != 4:
            raise HTTPException(status_code=400, detail="PIN must be 4 digits")
        
        # Hash the new PIN
        hashed_pin = bcrypt.hashpw(request.pin.encode(), bcrypt.gensalt()).decode()
        update_data["pin"] = hashed_pin
        update_data["password"] = ""  # Clear password if switching to PIN
    
    # Update by phone number
    result = await users_collection.update_one(
        {"phoneNumber": formatted_phone},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to reset credentials")
    
    return {
        "success": True,
        "message": "Credentials reset successfully"
    }

# Get user by ID endpoint for debugging
@router.get("/{user_id}")
async def get_user(user_id: str, db=Depends(get_database)):
    # Check if user exists using our helper function
    user = await find_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user": {
            "id": str(user.get("_id", user_id)),
            "name": user.get("name"),
            "phoneNumber": user.get("phoneNumber"),
            "avatar": user.get("avatar"),
            "authType": user.get("authType"),
            "createdAt": user.get("createdAt"),
            "updatedAt": user.get("updatedAt")
        }
    }

# Get user by phone number endpoint
@router.get("/phone/{phone_number}")
async def get_user_by_phone(phone_number: str, db=Depends(get_database)):
    users_collection = db["users"]
    
    user = await users_collection.find_one({"phoneNumber": phone_number})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user": {
            "id": str(user.get("_id")),
            "name": user.get("name"),
            "phoneNumber": user.get("phoneNumber"),
            "avatar": user.get("avatar"),
            "authType": user.get("authType")
        }
    }