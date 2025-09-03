# migrate_credentials.py
import asyncio
from app.services.database import get_database
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

async def migrate_credentials():
    try:
        db = await get_database()
        users = db['users']
        password_migrated = 0
        pin_migrated = 0
        skipped = 0
        
        print("Starting credentials migration...")
        
        async for user in users.find():
            user_id = user.get('_id')
            phone = user.get('phoneNumber', 'Unknown')
            updated_fields = {}
            
            # Check and migrate password
            password = user.get('password', '')
            if password and not password.startswith('$2b$'):
                hashed_password = pwd_context.hash(password)
                updated_fields['password'] = hashed_password
                print(f'✅ Password to migrate: {phone}')
            
            # Check and migrate PIN
            pin = user.get('pin', '')
            if pin and not pin.startswith('$2b$'):
                hashed_pin = pwd_context.hash(pin)
                updated_fields['pin'] = hashed_pin
                print(f'✅ PIN to migrate: {phone}')
            
            # Update if any fields need migration
            if updated_fields:
                result = await users.update_one(
                    {'_id': user_id},
                    {'$set': updated_fields}
                )
                
                if result.modified_count > 0:
                    if 'password' in updated_fields:
                        password_migrated += 1
                    if 'pin' in updated_fields:
                        pin_migrated += 1
                else:
                    print(f'❌ Failed to migrate: {phone}')
            else:
                skipped += 1
        
        print(f'\nMigration complete:')
        print(f'✅ Passwords migrated: {password_migrated}')
        print(f'✅ PINs migrated: {pin_migrated}')
        print(f'⏭️  Skipped (already hashed): {skipped}')
    
    except Exception as e:
        print(f'Error during migration: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(migrate_credentials())