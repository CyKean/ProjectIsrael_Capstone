import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()
FIREBASE = os.getenv('FIREBASE_CREDENTIALS')

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE)
    firebase_admin.initialize_app(cred)

db = firestore.client()
