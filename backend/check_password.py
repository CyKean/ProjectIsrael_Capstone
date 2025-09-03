# check_passwords.py
import asyncio
from app.services.database import get_database

async def check_password_status():
    try:
        db = await get_database()
        users = db['users']
        
        plaintext_count = 0
        hashed_count = 0
        empty_count = 0
        
        async for user in users.find():
            password = user.get('password', '')
            phone = user.get('phoneNumber', 'Unknown')
            
            if not password:
                print(f"📭 Empty: {phone}")
                empty_count += 1
            elif password.startswith('$2b$'):
                print(f"✅ Hashed: {phone}")
                hashed_count += 1
            else:
                print(f"📄 Plaintext: {phone} -> '{password}'")
                plaintext_count += 1
        
        print(f"\nSummary:")
        print(f"📄 Plaintext passwords: {plaintext_count}")
        print(f"✅ Hashed passwords: {hashed_count}")
        print(f"📭 Empty passwords: {empty_count}")
    
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_password_status())