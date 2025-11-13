import json
import random
from datetime import datetime

def generate_object_id():
    """Generate a MongoDB-like ObjectId string"""
    hex_chars = '0123456789abcdef'
    return ''.join(random.choice(hex_chars) for _ in range(24))

print('// === GENERATING SEGREGATED DATA FOR SEPTEMBER 20-30, 2024 ===')
print('// Copy and paste these data dictionaries:')
print('')

# Generate data for September 20-30, 2024
records_per_day = 4  # 4 records per day x 11 days = 44 total records

# Separate lists for each device type
npk_records = []
env_records = []
water_records = []

for day in range(20, 31):  # 20 to 30 inclusive
    date_str = f'2024-09-{day:02d}'
    
    for i in range(records_per_day):
        # Generate random time for this record
        hours = random.randint(0, 23)
        minutes = random.randint(0, 59)
        date_obj = datetime(2024, 9, day, hours, minutes, 0)
        timestamp_sec = int(date_obj.timestamp())
        
        # Generate NPK data (every 1st record)
        if i % 3 == 0:
            npk_record = {
                "_id": generate_object_id(),
                "device_id": "ESP32-NPKPH",
                "timestamp": {
                    "_seconds": timestamp_sec,
                    "_nanoseconds": random.randint(0, 999999999)
                },
                "nitrogen": random.randint(80, 200),  # 80-200
                "phosphorus": random.randint(150, 400),  # 150-400
                "potassium": random.randint(200, 400),  # 200-400
                "soilPh": round(4.0 + random.random() * 3.5, 1)  # 4.0-7.5
            }
            npk_records.append(npk_record)
        
        # Generate ENV data (every 2nd record)
        elif i % 3 == 1:
            env_record = {
                "_id": generate_object_id(),
                "device_id": "ESP32-ENV",
                "timestamp": {
                    "_seconds": timestamp_sec,
                    "_nanoseconds": random.randint(0, 999999999)
                },
                "soilMoisture": random.randint(30, 100),  # 30-100
                "temperature": round(25.0 + random.random() * 15.0, 1),  # 25.0-40.0
                "humidity": round(40.0 + random.random() * 40.0, 1)  # 40.0-80.0
            }
            env_records.append(env_record)
        
        # Generate WATER data (every 3rd record)
        else:
            water_record = {
                "_id": generate_object_id(),
                "device_id": "ESP32-WATERLVL",
                "waterLevel": round(60.0 + random.random() * 35.0, 1),  # 60.0-95.0
                "timestamp": {
                    "_seconds": timestamp_sec,
                    "_nanoseconds": random.randint(0, 999999999)
                }
            }
            water_records.append(water_record)

# Print NPK Records
print('// ===== ESP32-NPKPH RECORDS =====')
print('// NPK Sensor Data (15 records)')
for record in npk_records:
    print(json.dumps(record, indent=2) + ',')
    print('')

# Print ENV Records
print('// ===== ESP32-ENV RECORDS =====')
print('// Environmental Sensor Data (15 records)')
for record in env_records:
    print(json.dumps(record, indent=2) + ',')
    print('')

# Print WATER Records
print('// ===== ESP32-WATERLVL RECORDS =====')
print('// Water Level Sensor Data (14 records)')
for record in water_records:
    print(json.dumps(record, indent=2) + ',')
    print('')

print('// === SUMMARY ===')
print(f'// Total NPK records: {len(npk_records)}')
print(f'// Total ENV records: {len(env_records)}')
print(f'// Total WATER records: {len(water_records)}')
print(f'// Grand total: {len(npk_records) + len(env_records) + len(water_records)} records')
print('// Date range: September 20-30, 2024')