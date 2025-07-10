import firebase_admin
from firebase_admin import credentials, auth, firestore
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load Firebase credentials dynamically
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
if not FIREBASE_CREDENTIALS:
    raise ValueError("Firebase credentials not found. Set FIREBASE_CREDENTIALS in .env")

# Initialize Firebase App (Singleton)
if not firebase_admin._apps:  # Prevent re-initialization
    cred = credentials.Certificate(FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# Function to generate verification code
import random
import string

def generate_verification_code(length=6):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Function to send verification email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # Change to 587
SMTP_USERNAME = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = SMTP_USERNAME

print("SMTP Email:", SMTP_USERNAME)
print("SMTP Password:", "Loaded" if SMTP_PASSWORD else "Not Loaded")


# this part will be edited if you want to modify the email template
def send_verification_email(email, verification_code):
    subject = "Verify Your Email - Crop Recommendation System"
    body = f"""
    <html>
        <body>
            <h2>Email Verification</h2>
            <p>Hello,</p>
            <p>Thank you for registering. Please use the following verification code to verify your email:</p>
            <h3>{verification_code}</h3>
            <p>If you did not request this, please ignore this email.</p>
            <p>Best Regards,<br>Crop Recommendation Team</p>
        </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        # Use Port 587 with starttls()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, msg.as_string())

        print(f"✅ Verification email sent to {email}")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def forgot_password_verification_email(email, verification_code):
    subject = "Verify Your Email - Crop Recommendation System"
    body = f"""
    <html>
        <body>
            <h2>Forgot Password</h2>
            <p>Hello,</p>
            <p>Thank you for registering. Please use the following verification code to verify your email:</p>
            <h3>{verification_code}</h3>
            <p>If you did not request this, please ignore this email.</p>
            <p>Best Regards,<br>Crop Recommendation Team</p>
        </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        # Use Port 587 with starttls()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, msg.as_string())

        print(f"✅ Verification email sent to {email}")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def send_login_notification(email: str):
    """ Send an email to notify the user about the successful login """
    try:
        # Create the message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = email
        msg['Subject'] = "Login Notification"
        
        # Email body
        body = "You have successfully logged into the system."
        msg.attach(MIMEText(body, 'plain'))

        # Set up the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SMTP_USERNAME, SMTP_PASSWORD)  # Login to the email server
            server.sendmail(SENDER_EMAIL, email, msg.as_string())  # Send the email
            print(f"Notification sent to {email}")

    except Exception as e:
        print(f"Error sending email: {e}")

def send_otp_to_phone(phone: str):
    """Send OTP using Firebase Authentication"""
    try:
        # Create a temporary Firebase user with the phone number
        user = auth.get_user_by_phone_number(phone)
    except auth.UserNotFoundError:
        user = auth.create_user(phone_number=phone)

    # Generate a custom token (optional)
    custom_token = auth.create_custom_token(user.uid)

    # In Firebase Authentication, OTPs are sent from the frontend using signInWithPhoneNumber()
    print(f"✅ Firebase OTP initiated for {phone}")
    
    return {"message": "OTP request initiated. Complete authentication on the frontend.", "customToken": custom_token}
