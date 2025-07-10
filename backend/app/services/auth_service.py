from firebase_admin import auth
from app.services.firebase_service import db
from datetime import datetime
from fastapi import HTTPException

def register_user(first_name: str, last_name: str, email: str, password: str, accept_terms: bool):
    try:
        # Ensure terms are accepted
        if not accept_terms:
            raise HTTPException(status_code=400, detail="You must accept the terms and conditions.")

        # Create Firebase Auth User
        user = auth.create_user(email=email, password=password)

        # Store user details in Firestore
        user_data = {
            "uid": user.uid,
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "createdAt": datetime.utcnow().isoformat(),
            "verified": False  # Email verification step required
        }
        db.collection("users").document(user.uid).set(user_data)  # ✅ Correct Firestore reference

        return {"message": "User registered successfully", "userId": user.uid}
    
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Email already exists.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
