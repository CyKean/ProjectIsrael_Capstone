from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, field_validator
from typing import Optional, Any
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from app.services.database import get_database
from bson import ObjectId
import re
import os
import random
from dotenv import load_dotenv

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Load environment variables
load_dotenv()

# Security configuration - Get from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
if SECRET_KEY == "dev-secret-key-change-in-production":
    print("⚠️  WARNING: Using default SECRET_KEY. Change this in production!")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# Pydantic Models
class LoginRequest(BaseModel):
    phoneNumber: str
    credential: str
    authType: str  # "password" or "pin"

class RegisterRequest(BaseModel):
    phoneNumber: str
    credential: str
    authType: str  # "password" or "pin"

class OTPRequest(BaseModel):
    phoneNumber: str

class VerifyOTPRequest(BaseModel):
    phoneNumber: str
    otp: str

class UpdateAvatarRequest(BaseModel):
    avatarId: int

class ForgotPasswordRequest(BaseModel):
    phoneNumber: str

class VerifyResetCodeRequest(BaseModel):
    phoneNumber: str
    otp: str

class ResetPasswordRequest(BaseModel):
    phoneNumber: str
    authType: str  # "password" or "pin"
    newPassword: Optional[str] = None
    newPin: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    phoneNumber: str
    email: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    verified: bool
    createdAt: datetime
    avatar: Optional[dict] = None

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True

    @field_validator('createdAt', mode='before')
    @classmethod
    def convert_timestamp_to_datetime(cls, value):
        """
        Convert MongoDB timestamp to Python datetime
        Handles both datetime objects and MongoDB timestamp dictionaries
        """
        if value is None:
            return datetime.utcnow()
            
        # If it's already a datetime object, return as-is
        if isinstance(value, datetime):
            return value
            
        # If it's a MongoDB timestamp dictionary
        if isinstance(value, dict) and '_seconds' in value:
            # Convert from MongoDB timestamp format: {'_seconds': 123456789, '_nanoseconds': 0}
            seconds = value['_seconds']
            nanoseconds = value.get('_nanoseconds', 0)
            return datetime.fromtimestamp(seconds + nanoseconds / 1e9)
            
        # If it's a Unix timestamp (integer or float)
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value)
            
        # If it's a string, try to parse it
        if isinstance(value, str):
            try:
                # Handle ISO format strings
                if 'Z' in value:
                    value = value.replace('Z', '+00:00')
                return datetime.fromisoformat(value)
            except (ValueError, AttributeError):
                pass
                
        # Fallback to current time if conversion fails
        return datetime.utcnow()

# Utility Functions
def verify_password(plain_password, stored_hash):
    """
    Verify password with support for hashed and plaintext (for migration)
    """
    if not stored_hash:
        return False
    
    # If it's a bcrypt hash
    if stored_hash.startswith("$2b$"):
        try:
            return pwd_context.verify(plain_password, stored_hash)
        except:
            return False
    
    # If it's plaintext (for migration)
    if stored_hash == plain_password:
        return True
    
    return False

def verify_pin(plain_pin, stored_pin):
    """
    Verify PIN with support for hashed and plaintext (for migration)
    """
    if not stored_pin:
        return False
    
    # If it's a bcrypt hash
    if stored_pin.startswith("$2b$"):
        try:
            return pwd_context.verify(plain_pin, stored_pin)
        except:
            return False
    
    # If it's plaintext (for migration)
    if stored_pin == plain_pin:
        return True
    
    return False

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def is_valid_philippine_phone_number(phone_number):
    pattern = r"^(\+639|09)\d{9}$"
    return re.match(pattern, phone_number) is not None

def to_e164_format(phone_number):
    cleaned = phone_number.replace(" ", "").replace("-", "")
    if cleaned.startswith("+63"):
        return cleaned
    elif cleaned.startswith("09"):
        return "+63" + cleaned[1:]
    elif cleaned.startswith("63"):
        return "+" + cleaned
    return None

def generate_otp(length: int = 6) -> str:
    """Generate a random numeric OTP"""
    return ''.join(random.choices('0123456789', k=length))

def get_avatar_options():
    """Return available avatar options matching the frontend"""
    return [
        {"id": 1, "icon": "🌱", "name": "Seedling"},
        {"id": 2, "icon": "🌿", "name": "Herb"},
        {"id": 3, "icon": "🌾", "name": "Wheat"},
        {"id": 4, "icon": "🌽", "name": "Corn"},
        {"id": 5, "icon": "🥕", "name": "Carrot"},
        {"id": 6, "icon": "🍅", "name": "Tomato"},
        {"id": 7, "icon": "🥬", "name": "Lettuce"},
        {"id": 8, "icon": "🌻", "name": "Sunflower"},
        {"id": 9, "icon": "🌳", "name": "Tree"},
        {"id": 10, "icon": "🍃", "name": "Leaves"},
        {"id": 11, "icon": "🌵", "name": "Cactus"},
        {"id": 12, "icon": "🌸", "name": "Blossom"},
        {"id": 13, "icon": "🍄", "name": "Mushroom"},
        {"id": 14, "icon": "🌺", "name": "Hibiscus"},
        {"id": 15, "icon": "🌹", "name": "Rose"},
        {"id": 16, "icon": "🌷", "name": "Tulip"},
        {"id": 17, "icon": "🥦", "name": "Broccoli"},
        {"id": 18, "icon": "🌶️", "name": "Pepper"},
        {"id": 19, "icon": "🥒", "name": "Cucumber"},
        {"id": 20, "icon": "🍆", "name": "Eggplant"},
        {"id": 21, "icon": "🥔", "name": "Potato"},
        {"id": 22, "icon": "🧄", "name": "Garlic"},
        {"id": 23, "icon": "🧅", "name": "Onion"},
        {"id": 24, "icon": "🥜", "name": "Peanut"}
    ]

def get_random_avatar():
    """Return a random avatar object from available options"""
    avatars = get_avatar_options()
    return random.choice(avatars)

def get_avatar_by_id(avatar_id: int):
    """Get specific avatar by ID"""
    avatars = get_avatar_options()
    for avatar in avatars:
        if avatar["id"] == avatar_id:
            return avatar
    return get_random_avatar()  # Fallback to random if ID not found

def convert_mongo_timestamp(timestamp):
    """Convert MongoDB timestamp to Python datetime"""
    if isinstance(timestamp, dict) and '_seconds' in timestamp:
        seconds = timestamp['_seconds']
        nanoseconds = timestamp.get('_nanoseconds', 0)
        return datetime.fromtimestamp(seconds + nanoseconds / 1e9)
    elif isinstance(timestamp, datetime):
        return timestamp
    else:
        return datetime.utcnow()

# Authentication dependency (moved to top)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        # Check token expiration
        exp = payload.get("exp")
        if exp and datetime.utcnow() > datetime.utcfromtimestamp(exp):
            raise HTTPException(status_code=401, detail="Token has expired")
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    db = await get_database()
    users_collection = db["users"]
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

# Routes
@router.post("/login")
async def login(login_request: LoginRequest):
    db = await get_database()
    users_collection = db["users"]
    
    # Validate phone number
    if not is_valid_philippine_phone_number(login_request.phoneNumber):
        raise HTTPException(status_code=400, detail="Invalid Philippine phone number")
    
    formatted_phone = to_e164_format(login_request.phoneNumber)
    if not formatted_phone:
        raise HTTPException(status_code=400, detail="Could not format phone number")
    
    # Find user by phone number
    user = await users_collection.find_one({"phoneNumber": formatted_phone})
    if not user:
        raise HTTPException(status_code=404, detail="No account found with this phone number")
    
    # Check if account is verified
    if not user.get("verified", False):
        raise HTTPException(status_code=401, detail="Account is not verified")
    
    # Verify credentials based on auth type
    if login_request.authType == "password":
        stored_password = user.get("password")
        if not stored_password:
            raise HTTPException(status_code=401, detail="Password not set for this account")
        
        if not verify_password(login_request.credential, stored_password):
            raise HTTPException(status_code=401, detail="Incorrect password")
            
        # Migrate plaintext password to hash if needed
        if stored_password and not stored_password.startswith("$2b$"):
            hashed_password = get_password_hash(login_request.credential)
            await users_collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"password": hashed_password}}
            )
            print(f"✅ Migrated password to bcrypt for {formatted_phone}")
            
    elif login_request.authType == "pin":
        stored_pin = user.get("pin")
        if not stored_pin:
            raise HTTPException(status_code=401, detail="PIN not set for this account")
        
        if not verify_pin(login_request.credential, stored_pin):
            raise HTTPException(status_code=401, detail="Incorrect PIN")
            
        # Migrate plaintext PIN to hash if needed
        if stored_pin and not stored_pin.startswith("$2b$"):
            hashed_pin = get_password_hash(login_request.credential)
            await users_collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"pin": hashed_pin}}
            )
            print(f"✅ Migrated PIN to bcrypt for {formatted_phone}")
            
    else:
        raise HTTPException(status_code=400, detail="Invalid authentication type")
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user["_id"])}, expires_delta=access_token_expires
    )
    
    # Prepare user response (excluding sensitive data)
    user_response = UserResponse(
        id=str(user["_id"]),
        phoneNumber=user["phoneNumber"],
        email=user.get("email"),
        firstName=user.get("firstName"),
        lastName=user.get("lastName"),
        verified=user.get("verified", False),
        createdAt=user.get("createdAt", datetime.utcnow()),
        avatar=user.get("avatar")
    )
    
    return {
        "success": True,
        "message": "Login successful",
        "user": user_response,
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/register")
async def register_user(register_request: RegisterRequest):
    db = await get_database()
    users_collection = db["users"]
    
    # Validate phone number
    if not is_valid_philippine_phone_number(register_request.phoneNumber):
        raise HTTPException(status_code=400, detail="Invalid Philippine phone number")
    
    formatted_phone = to_e164_format(register_request.phoneNumber)
    if not formatted_phone:
        raise HTTPException(status_code=400, detail="Could not format phone number")
    
    # Validate credential
    if not register_request.credential or not register_request.credential.strip():
        raise HTTPException(status_code=400, detail=f"Please enter your {register_request.authType}")
    
    if register_request.authType == "pin" and len(register_request.credential) != 4:
        raise HTTPException(status_code=400, detail="PIN must be exactly 4 digits")
    
    # Check if user already exists
    existing_user = await users_collection.find_one({"phoneNumber": formatted_phone})
    
    otp = generate_otp()
    avatar = get_random_avatar()
    current_time = datetime.utcnow()
    
    if existing_user:
        # User exists, check if already verified
        if existing_user.get("verified", False):
            raise HTTPException(status_code=400, detail="Phone number already registered and verified")
        
        # Update existing unverified user
        update_data = {
            "authType": register_request.authType,
            "otp": otp,
            "otpSentAt": current_time,
            "avatar": avatar,
            "updatedAt": current_time
        }
        
        # Set password or pin based on auth type
        if register_request.authType == "password":
            update_data["password"] = get_password_hash(register_request.credential)
            update_data["pin"] = ""  # Clear pin if switching to password
        else:
            update_data["pin"] = get_password_hash(register_request.credential)
            update_data["password"] = ""  # Clear password if switching to pin
        
        await users_collection.update_one(
            {"_id": existing_user["_id"]},
            {"$set": update_data}
        )
        
        user_id = str(existing_user["_id"])
        action = "updated"
        
    else:
        # Create new user
        user_data = {
            "phoneNumber": formatted_phone,
            "authType": register_request.authType,
            "otp": otp,
            "otpSentAt": current_time,
            "verified": False,
            "avatar": avatar,
            "createdAt": current_time,
            "updatedAt": current_time
        }
        
        # Set password or pin based on auth type
        if register_request.authType == "password":
            user_data["password"] = get_password_hash(register_request.credential)
            user_data["pin"] = ""
        else:
            user_data["pin"] = get_password_hash(register_request.credential)
            user_data["password"] = ""
        
        result = await users_collection.insert_one(user_data)
        user_id = str(result.inserted_id)
        action = "created"
    
    # Log OTP for testing (replace with actual SMS integration)
    print(f"📱 OTP for {formatted_phone}: {otp}")
    
    return {
        "success": True,
        "message": f"User {action} successfully. OTP sent.",
        "userId": user_id,
        "phoneNumber": formatted_phone,
        "avatar": avatar,
        "otp": otp  # Remove this in production - only for testing
    }

@router.post("/verify-otp")
async def verify_otp(verify_request: VerifyOTPRequest):
    db = await get_database()
    users_collection = db["users"]
    
    formatted_phone = to_e164_format(verify_request.phoneNumber)
    if not formatted_phone:
        raise HTTPException(status_code=400, detail="Invalid phone number format")
    
    # Find user by phone number
    user = await users_collection.find_one({"phoneNumber": formatted_phone})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if already verified
    if user.get("verified", False):
        raise HTTPException(status_code=400, detail="User already verified")
    
    # Check OTP
    stored_otp = user.get("otp")
    otp_sent_at = user.get("otpSentAt")
    
    if not stored_otp or not otp_sent_at:
        raise HTTPException(status_code=400, detail="No OTP found for this user")
    
    # Check OTP expiration (15 minutes)
    otp_sent_time = convert_mongo_timestamp(otp_sent_at)
    if datetime.utcnow() > otp_sent_time + timedelta(minutes=15):
        raise HTTPException(status_code=400, detail="OTP has expired")
    
    if verify_request.otp != stored_otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    # Verify the user
    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {
            "verified": True,
            "verifiedAt": datetime.utcnow(),
            "otp": None,  # Clear OTP after verification
            "updatedAt": datetime.utcnow()
        }}
    )
    
    return {
        "success": True,
        "message": "Phone number verified successfully"
    }

@router.post("/resend-otp")
async def resend_otp(otp_request: OTPRequest):
    db = await get_database()
    users_collection = db["users"]
    
    formatted_phone = to_e164_format(otp_request.phoneNumber)
    if not formatted_phone:
        raise HTTPException(status_code=400, detail="Invalid phone number format")
    
    # Find user by phone number
    user = await users_collection.find_one({"phoneNumber": formatted_phone})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if already verified
    if user.get("verified", False):
        raise HTTPException(status_code=400, detail="User already verified")
    
    # Generate new OTP
    new_otp = generate_otp()
    current_time = datetime.utcnow()
    
    # Update user with new OTP
    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {
            "otp": new_otp,
            "otpSentAt": current_time,
            "updatedAt": current_time
        }}
    )
    
    # Log OTP for testing
    print(f"📱 New OTP for {formatted_phone}: {new_otp}")
    
    return {
        "success": True,
        "message": "New OTP sent successfully",
        "otp": new_otp  # Remove this in production - only for testing
    }

@router.get("/avatars")
async def get_all_avatars():
    """Get all available avatars"""
    return {
        "success": True,
        "avatars": get_avatar_options()
    }

@router.get("/avatars/{avatar_id}")
async def get_avatar(avatar_id: int):
    """Get specific avatar by ID"""
    avatar = get_avatar_by_id(avatar_id)
    return {
        "success": True,
        "avatar": avatar
    }

@router.put("/users/{user_id}/avatar")
async def update_user_avatar(user_id: str, avatar_request: UpdateAvatarRequest, current_user: dict = Depends(get_current_user)):
    """Update user's avatar"""
    # Verify the user is updating their own profile
    if user_id != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Cannot update other user's avatar")
    
    avatar_id = avatar_request.avatarId
    avatar = get_avatar_by_id(avatar_id)
    
    db = await get_database()
    users_collection = db["users"]
    
    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {
            "avatar": avatar,
            "updatedAt": datetime.utcnow()
        }}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found or avatar unchanged")
    
    return {
        "success": True,
        "message": "Avatar updated successfully",
        "avatar": avatar
    }

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    """Send password reset OTP to user's phone"""
    db = await get_database()
    users_collection = db["users"]
    
    # Validate phone number
    if not is_valid_philippine_phone_number(request.phoneNumber):
        raise HTTPException(status_code=400, detail="Invalid Philippine phone number")
    
    formatted_phone = to_e164_format(request.phoneNumber)
    if not formatted_phone:
        raise HTTPException(status_code=400, detail="Could not format phone number")
    
    # Check if user exists
    user = await users_collection.find_one({"phoneNumber": formatted_phone})
    if not user:
        raise HTTPException(status_code=404, detail="This phone number is not registered")
    
    # Check if user is verified
    if not user.get("verified", False):
        raise HTTPException(status_code=400, detail="Account not verified. Please verify your account first.")
    
    # Generate OTP
    otp = generate_otp()
    current_time = datetime.utcnow()
    
    try:
        
        # If SMS is successful, save OTP to database
        await users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {
                "otp": otp,
                "otpSentAt": current_time,
                "updatedAt": current_time
            }}
        )
        
        return {
            "success": True,
            "message": "Password reset code sent to your phone",
            "otp": otp  # Remove this in production
        }
        
    except Exception as e:
        print(f"❌ Error in forgot password: {e}")
        raise HTTPException(status_code=500, detail="Failed to process password reset request")

@router.post("/verify-reset-code")
async def verify_reset_code(request: VerifyResetCodeRequest):
    """Verify the password reset OTP"""
    db = await get_database()
    users_collection = db["users"]
    
    formatted_phone = to_e164_format(request.phoneNumber)
    if not formatted_phone:
        raise HTTPException(status_code=400, detail="Invalid phone number format")
    
    # Find user by phone number
    user = await users_collection.find_one({"phoneNumber": formatted_phone})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check OTP
    stored_otp = user.get("otp")
    otp_sent_at = user.get("otpSentAt")
    
    if not stored_otp:
        raise HTTPException(status_code=400, detail="No reset code found")
    
    # Check OTP expiration (15 minutes)
    otp_sent_time = convert_mongo_timestamp(otp_sent_at)
    if datetime.utcnow() > otp_sent_time + timedelta(minutes=15):
        raise HTTPException(status_code=400, detail="Reset code has expired")
    
    if request.otp != stored_otp:
        raise HTTPException(status_code=400, detail="Invalid reset code")
    
    # Clear OTP after successful verification
    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"otp": None}}
    )
    
    return {
        "success": True,
        "message": "Reset code verified successfully"
    }

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    """Reset user password or PIN"""
    db = await get_database()
    users_collection = db["users"]
    
    formatted_phone = to_e164_format(request.phoneNumber)
    if not formatted_phone:
        raise HTTPException(status_code=400, detail="Invalid phone number format")
    
    # Find user by phone number
    user = await users_collection.find_one({"phoneNumber": formatted_phone})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate credentials based on auth type
    if request.authType == "password":
        if not request.newPassword:
            raise HTTPException(status_code=400, detail="New password is required")
        if len(request.newPassword) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")
        
        hashed_password = get_password_hash(request.newPassword)
        update_data = {
            "password": hashed_password,
            "pin": "",  # Clear PIN when setting password
            "authType": "password",
            "updatedAt": datetime.utcnow()
        }
        
    elif request.authType == "pin":
        if not request.newPin:
            raise HTTPException(status_code=400, detail="New PIN is required")
        if not re.match(r'^\d{4}$', request.newPin):
            raise HTTPException(status_code=400, detail="PIN must be exactly 4 digits")
        
        hashed_pin = get_password_hash(request.newPin)
        update_data = {
            "pin": hashed_pin,
            "password": "",  # Clear password when setting PIN
            "authType": "pin",
            "updatedAt": datetime.utcnow()
        }
        
    else:
        raise HTTPException(status_code=400, detail="Invalid authentication type")
    
    # Update user credentials
    result = await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to reset credentials")
    
    return {
        "success": True,
        "message": "Credentials reset successfully"
    }

@router.post("/resend-reset-code")
async def resend_reset_code(request: ForgotPasswordRequest):
    """Resend password reset OTP"""
    db = await get_database()
    users_collection = db["users"]
    
    formatted_phone = to_e164_format(request.phoneNumber)
    if not formatted_phone:
        raise HTTPException(status_code=400, detail="Invalid phone number format")
    
    # Find user by phone number
    user = await users_collection.find_one({"phoneNumber": formatted_phone})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate new OTP
    new_otp = generate_otp()
    current_time = datetime.utcnow()
    
    try:
        # Send SMS first
        sms_success = await send_password_reset_sms(formatted_phone, new_otp)
        
        if not sms_success:
            raise HTTPException(status_code=500, detail="Failed to send OTP via SMS")
        
        # Update OTP in database
        await users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {
                "otp": new_otp,
                "otpSentAt": current_time,
                "updatedAt": current_time
            }}
        )
        
        return {
            "success": True,
            "message": "New reset code sent to your phone",
            "otp": new_otp  # Remove this in production
        }
        
    except Exception as e:
        print(f"❌ Error resending reset code: {e}")
        raise HTTPException(status_code=500, detail="Failed to resend reset code")

# Additional endpoints for testing and token management
@router.get("/test")
async def test_auth():
    return {"message": "Auth endpoint is working!", "status": "success"}

@router.post("/refresh")
async def refresh_token(current_user: dict = Depends(get_current_user)):
    """Refresh an access token"""
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(current_user["_id"])}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    # Convert MongoDB document to Pydantic model
    user_response = UserResponse(
        id=str(current_user["_id"]),
        phoneNumber=current_user["phoneNumber"],
        email=current_user.get("email"),
        firstName=current_user.get("firstName"),
        lastName=current_user.get("lastName"),
        verified=current_user.get("verified", False),
        createdAt=current_user.get("createdAt", datetime.utcnow()),
        avatar=current_user.get("avatar")
    )
    
    return user_response