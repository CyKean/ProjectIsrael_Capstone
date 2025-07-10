from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr  
from datetime import datetime, timedelta
from app.services.firebase_service import auth, db, send_verification_email, send_login_notification, firestore, forgot_password_verification_email, send_otp_to_phone
import random
import pytz
import re
import requests

router = APIRouter()


class RegisterUserRequest(BaseModel):
    firstName: str
    lastName: str
    email: str = None
    phone: str = None
    password: str
    acceptTerms: bool

def generate_verification_code(length=6):
    return "".join(str(random.randint(0, 9)) for _ in range(length))

@router.post("/register")
async def register_user(user: RegisterUserRequest):
    print("🚀 Incoming Request Data:", user.dict())  

    if not db:
        raise HTTPException(status_code=500, detail="Firebase Firestore not initialized")

    try:
        if not user.acceptTerms:
            raise HTTPException(status_code=400, detail="You must accept the terms and conditions.")

        auth_user = auth.create_user(email=user.email, password=user.password)
        uid = auth_user.uid  

        verification_code = generate_verification_code(6)

        expiration_time = datetime.utcnow() + timedelta(minutes=10)

        user_data = {
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "createdAt": datetime.utcnow().isoformat(),
            "verified": False,
            "verificationCode": verification_code,
            "verificationCodeExpiration": expiration_time.isoformat()
        }

        db.collection("users").document(uid).set(user_data)

        send_verification_email(user.email, verification_code)

        return {"message": "User registered successfully. Check your email for verification.", "userId": uid}

    except auth.EmailAlreadyExistsError:
        print("❌ Error: Email already exists")
        raise HTTPException(status_code=400, detail="Email already exists.")

    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}") 
        raise HTTPException(status_code=500, detail=str(e))

class ResendCodeRequest(BaseModel):
    uid: str

@router.post("/resend-code")
async def resend_code(data: ResendCodeRequest):
    print("📩 Received Resend Code Request:", data.dict()) 
    uid = data.uid
    if not uid:
        raise HTTPException(status_code=400, detail="UID is required.")
    
    user_ref = db.collection("users").document(uid)
    user_data = user_ref.get()

    if not user_data.exists:
        raise HTTPException(status_code=404, detail="User not found")

    user_info = user_data.to_dict()

    if user_info["verified"]:
        return {"message": "User is already verified"}

    expiration_time = user_info.get("verificationCodeExpiration")
    if expiration_time:
        expiration_time = datetime.fromisoformat(expiration_time)
        if datetime.utcnow() > expiration_time:
            raise HTTPException(status_code=400, detail="Verification code has expired. Request a new one.")

    new_verification_code = generate_verification_code(6)
    new_expiration_time = datetime.utcnow() + timedelta(minutes=10)  
    user_ref.update({
        "verificationCode": new_verification_code,
        "verificationCodeExpiration": new_expiration_time.isoformat()
    })

    send_verification_email(user_info["email"], new_verification_code)
    
    return {"message": "New verification code sent"}
    
class VerifyEmailRequest(BaseModel):
    uid: str
    code: str

@router.post("/verify-email")
async def verify_email(data: VerifyEmailRequest):
    uid = data.uid
    code = data.code

    user_ref = db.collection("users").document(uid)
    user_data = user_ref.get()

    if not user_data.exists:
        raise HTTPException(status_code=404, detail="User not found")

    user_info = user_data.to_dict()

    if user_info["verified"]:
        return {"message": "User is already verified"}

    if user_info["verificationCode"] != code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    user_ref.update({
        "verified": True,
        "verificationCode": firestore.DELETE_FIELD
    })

    return {"message": "Email successfully verified"}

from dotenv import load_dotenv
import os

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
async def login_user(data: LoginRequest):
    try:
        FIREBASE_API_KEY = os.getenv("API_KEY")
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
        payload = {
            "email": data.email,
            "password": data.password,
            "returnSecureToken": True
        }
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers)
        res_data = response.json()

        if "error" in res_data:
            raise HTTPException(status_code=400, detail=res_data["error"]["message"])

        user_id = res_data["localId"]
        user_ref = db.collection("users").document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            user_data = {
                "firstName": user_doc.firstName,
                "lastName": user_doc.lasttName,
                "email": data.email,
                "phone": "",
                "profilePicture": None 
            }
        else:
            user_data = user_doc.to_dict()

        send_login_notification(data.email)

        return {
            "message": "Login successful",
            "token": res_data["idToken"],
            "user": {
                "userId": user_id,
                "firstName": user_data.get("firstName", ""),
                "lastName": user_data.get("lastName", ""),
                "email": user_data.get("email", data.email), 
                "phone": user_data.get("phone", ""),
                "profilePicture": user_data.get("profilePicture"),  
            },
        }

    except Exception as e:
        print(f"❌ Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

@router.post("/google-register")
async def google_register(request: Request):
    try:
        body = await request.json()
        idToken = body.get("idToken")

        if not idToken:
            raise HTTPException(status_code=422, detail="idToken is required")

        decoded_token = auth.verify_id_token(idToken)
        uid = decoded_token.get("uid")
        email = decoded_token.get("email")
        name = decoded_token.get("name")
        picture = decoded_token.get("picture", None)  

        if not uid or not email:
            raise HTTPException(status_code=400, detail="Invalid Google user data")

        db_client = firestore.client()
        user_ref = db_client.collection("users").document(uid)
        user_doc = user_ref.get()

        if user_doc.exists:
            user_data = user_doc.to_dict()
            return {
                "message": "User already registered",
                "user": {
                    "userId": uid,
                    "name": user_data.get("name"),
                    "email": user_data.get("email"),
                    "profilePicture": user_data.get("profilePicture"),
                },
            }

        user_data = {
            "uid": uid,
            "name": name,
            "email": email,
            "profilePicture": picture or generate_profile_picture(email),
            "createdAt": datetime.utcnow().isoformat(),
            "verified": True, 
        }
        user_ref.set(user_data)

        send_login_notification(email)

        return {
            "message": "User registered successfully",
            "user": {
                "userId": uid,
                "name": user_data["name"],
                "email": user_data["email"],
                "profilePicture": user_data["profilePicture"],
                "createdAt": user_data["createdAt"],
            },
        }

    except Exception as e:
        print(f"❌ Firebase Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Google registration failed: {str(e)}")

def generate_profile_picture(email):
    import hashlib
    hashed_email = hashlib.md5(email.encode()).hexdigest()[:6]
    initials = email[0].upper()
    return f"https://dummyimage.com/100x100/000/fff.png&text={initials}"

@router.post("/google-login")
async def google_login(request: Request):
    try:
        body = await request.json()
        idToken = body.get("idToken")

        if not idToken:
            raise HTTPException(status_code=422, detail="idToken is required")

        # 🔹 Verify Firebase ID Token
        decoded_token = auth.verify_id_token(idToken)
        uid = decoded_token.get("uid")
        email = decoded_token.get("email")
        name = decoded_token.get("name")
        picture = decoded_token.get("picture", None)  # Google profile picture

        if not uid or not email:
            raise HTTPException(status_code=400, detail="Invalid Google user data")

        # 🔹 Firestore Database Connection
        db_client = firestore.client()
        user_ref = db_client.collection("users").document(uid)
        user_doc = user_ref.get()

        if not user_doc.exists:
            # If user is new, save to Firestore
            user_data = {
                "uid": uid,
                "name": name,
                "email": email,
                "profilePicture": picture or generate_profile_picture(email),  # Use default if missing
                "createdAt": firestore.SERVER_TIMESTAMP,
                "verified": True,
            }
            user_ref.set(user_data)
        else:
            user_data = user_doc.to_dict()

        # 🔹 Return full user details
        return {
            "message": "Login successful",
            "user": {
                "userId": uid,
                "name": user_data.get("name"),
                "email": user_data.get("email"),
                "profilePicture": user_data.get("profilePicture"),
            },
        }

    except Exception as e:
        print(f"❌ Google Login Error: {str(e)}")  # Debugging logs
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

# ✅ Helper Function to Generate Default Profile Picture (Initials)
def generate_profile_picture(email):
    import hashlib
    hashed_email = hashlib.md5(email.encode()).hexdigest()[:6]  # Unique identifier
    initials = email[0].upper()  # Use first letter as default profile
    return f"https://dummyimage.com/100x100/000/fff.png&text={initials}"



# Request model for forgot password
class ForgotPasswordRequest(BaseModel):
    email: str

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    try:
        # 🔹 Check if user exists
        try:
            user = auth.get_user_by_email(request.email)
        except auth.UserNotFoundError:
            raise HTTPException(status_code=400, detail="User not found")

        # 🔹 Generate a random 6-digit verification code
        verification_code = generate_verification_code(6)

        # 🔹 Set explicit expiration time (10 minutes from now)
        expiration_time = datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(minutes=10)

        # 🔹 Store the code in Firestore
        db.collection("password_reset_codes").document(request.email).set({
            "code": verification_code,
            "expires_at": expiration_time.strftime("%Y-%m-%d %H:%M:%S.%f%z")  # Store as string to avoid Firestore timezone issues
        })

        # 🔹 Send the code via email
        forgot_password_verification_email(request.email, verification_code)

        return {"message": "Verification code sent to your email"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class VerifyCodeRequest(BaseModel):
    email: str
    code: str
# ✅ Step 2: Verify the 6-digit code
@router.post("/verify-code")
async def verify_code(request: VerifyCodeRequest):
    try:
        # Fetch the document from Firestore
        doc_ref = db.collection("password_reset_codes").document(request.email)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=400, detail="No verification code found. Request a new one.")

        stored_data = doc.to_dict()
        stored_code = stored_data.get("code")
        expires_at = stored_data.get("expires_at")  # Get expiration timestamp

        # Log the stored and entered codes for debugging
        print(f"Stored code: {stored_code}")
        print(f"Entered code: {request.code}")

        # 🔹 Convert Firestore timestamp to Python datetime
        if expires_at:
            if isinstance(expires_at, str):  # If the value is a string, parse it as a datetime
                expires_at_dt = datetime.fromisoformat(expires_at)
            else:
                expires_at_dt = expires_at.to_pydatetime()  # Convert Firestore timestamp to Python datetime
            
            current_time = datetime.utcnow().replace(tzinfo=pytz.UTC)  # Get current time with timezone info

            # 🔹 Check if the code is expired
            if current_time > expires_at_dt:
                raise HTTPException(status_code=400, detail="Verification code expired. Request a new one.")

        # 🔹 Validate code
        if stored_code != request.code:
            raise HTTPException(status_code=400, detail="Invalid verification code. Please check and try again.")

        return {"message": "Verification successful"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    try:
        # Get the password reset code document
        doc_ref = db.collection("password_reset_codes").document(request.email)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=400, detail="No verification code found. Request a new one.")

        # Update the password in Firebase Authentication
        try:
            user = auth.get_user_by_email(request.email)
            auth.update_user(user.uid, password=request.new_password)
        except auth.UserNotFoundError:
            raise HTTPException(status_code=404, detail="User not found in Firebase Authentication.")

        return {"message": "Password successfully updated."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))