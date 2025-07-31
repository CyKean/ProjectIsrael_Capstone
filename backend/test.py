import requests

# Replace these with your actual bot token and chat/user ID
TELEGRAM_BOT_TOKEN = "7961729220:AAFKIdgCFtNuMjlkuQssqUBZLjeXTmYIhnY"
TELEGRAM_CHAT_ID = "6085990774"  # Your Telegram user ID (not bot username)

# Message you want to send to your bot
number = "+639123456789"
otp_message = "Your OTP is 123456"
text_to_send = f"SMS::{number}::{otp_message}"

# Telegram Bot API URL
url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# Send the message
response = requests.post(
    url,
    json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text_to_send
    }
)

# Check result
if response.status_code == 200:
    print("✅ Message sent successfully.")
else:
    print(f"❌ Failed to send. Status: {response.status_code}, Response: {response.text}")
