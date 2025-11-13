import pymongo
from datetime import datetime, timedelta
import random
import time
from pymongo import UpdateOne, DeleteMany

class MongoDBDataManager:
    def __init__(self, host='localhost', port=27017, db_name='projectisrael_db'):
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client[db_name]
        self.sensor_readings = self.db['sensor_readings']
        self.water_level_readings = self.db['water_level_readings']
        
        # Device configurations
        self.sensor_devices = {
            'esp32-1': {
                'type': 'nutrients',
                'fields': ['nitrogen', 'phosphorus', 'potassium', 'soilPh'],
                'ranges': {
                    'nitrogen': (40, 80),
                    'phosphorus': (120, 200),
                    'potassium': (100, 180),
                    'soilPh': (3.0, 7.0)
                }
            },
            'esp32-2': {
                'type': 'environment',
                'fields': ['soilMoisture', 'temperature', 'humidity'],
                'ranges': {
                    'soilMoisture': (60, 100),
                    'temperature': (25.0, 40.0),
                    'humidity': (50.0, 80.0)
                }
            }
        }
        
        self.water_level_device = {
            'device_id': 'ESP32-WATERLVL',
            'range': (80.0, 120.0)
        }
    
    def generate_timestamp(self, date, time_offset_minutes=0):
        """Generate a timestamp for a specific date with random time"""
        base_time = datetime(date.year, date.month, date.day)
        random_time = base_time + timedelta(minutes=time_offset_minutes)
        return {
            '_seconds': int(random_time.timestamp()),
            '_nanoseconds': random.randint(0, 999999999)
        }
    
    def generate_sensor_reading(self, device_id, timestamp):
        """Generate sensor reading data based on device type"""
        device_config = self.sensor_devices[device_id]
        reading = {'timestamp': timestamp}
        
        for field, value_range in device_config['ranges'].items():
            if field in ['soilPh', 'temperature', 'humidity']:
                # Float values
                reading[field] = round(random.uniform(value_range[0], value_range[1]), 1)
            else:
                # Integer values
                reading[field] = random.randint(value_range[0], value_range[1])
        
        return reading
    
    def generate_water_level_reading(self, timestamp):
        """Generate water level reading data"""
        return {
            'device_id': self.water_level_device['device_id'],
            'waterLevel': round(random.uniform(*self.water_level_device['range']), 1),
            'timestamp': timestamp
        }
    
    def iterative_fetch_dates(self, collection, start_date, end_date, batch_size=1000):
        """Iteratively fetch dates from collection to avoid timeout"""
        current_date = start_date
        all_dates_data = {}
        
        while current_date <= end_date:
            next_date = current_date + timedelta(days=7)  # Process one week at a time
            if next_date > end_date:
                next_date = end_date
            
            print(f"Processing dates from {current_date} to {next_date}")
            
            # For sensor_readings collection
            if collection == self.sensor_readings:
                pipeline = [
                    {'$unwind': '$readings'},
                    {'$match': {
                        'readings.timestamp._seconds': {
                            '$gte': int(current_date.timestamp()),
                            '$lte': int(next_date.timestamp())
                        }
                    }},
                    {'$group': {
                        '_id': {
                            'date': {
                                '$dateToString': {
                                    'format': '%Y-%m-%d',
                                    'date': {
                                        '$toDate': {
                                            '$multiply': ['$readings.timestamp._seconds', 1000]
                                        }
                                    }
                                }
                            },
                            'device_id': '$_id'
                        },
                        'count': {'$sum': 1},
                        'readings': {'$push': '$readings'}
                    }},
                    {'$batchSize': batch_size}
                ]
                
                results = list(collection.aggregate(pipeline))
                for result in results:
                    date_str = result['_id']['date']
                    device_id = result['_id']['device_id']
                    
                    if date_str not in all_dates_data:
                        all_dates_data[date_str] = {}
                    
                    all_dates_data[date_str][device_id] = {
                        'count': result['count'],
                        'readings': result['readings']
                    }
            
            # For water_level_readings collection
            elif collection == self.water_level_readings:
                pipeline = [
                    {'$match': {
                        'timestamp._seconds': {
                            '$gte': int(current_date.timestamp()),
                            '$lte': int(next_date.timestamp())
                        }
                    }},
                    {'$group': {
                        '_id': {
                            '$dateToString': {
                                'format': '%Y-%m-%d',
                                'date': {
                                    '$toDate': {
                                        '$multiply': ['$timestamp._seconds', 1000]
                                    }
                                }
                            }
                        },
                        'count': {'$sum': 1},
                        'readings': {'$push': '$$ROOT'}
                    }},
                    {'$batchSize': batch_size}
                ]
                
                results = list(collection.aggregate(pipeline))
                for result in results:
                    date_str = result['_id']
                    all_dates_data[date_str] = {
                        'count': result['count'],
                        'readings': result['readings']
                    }
            
            current_date = next_date + timedelta(days=1)
            time.sleep(0.1)  # Small delay to prevent overwhelming the database
        
        return all_dates_data
    
    def normalize_sensor_readings(self, target_days=200):
        """Normalize sensor readings data"""
        start_date = datetime(2025, 9, 26)
        end_date = datetime(2025, 10, 31)
        
        print("Fetching sensor readings data...")
        dates_data = self.iterative_fetch_dates(self.sensor_readings, start_date, end_date)
        
        operations = []
        
        for single_date in self.date_range(start_date, end_date):
            date_str = single_date.strftime('%Y-%m-%d')
            
            for device_id in self.sensor_devices.keys():
                current_count = 0
                existing_readings = []
                
                if date_str in dates_data and device_id in dates_data[date_str]:
                    current_count = dates_data[date_str][device_id]['count']
                    existing_readings = dates_data[date_str][device_id]['readings']
                
                if current_count == 0:
                    # No data for this date - generate full day
                    print(f"Generating {target_days} readings for {device_id} on {date_str}")
                    new_readings = []
                    for i in range(target_days):
                        timestamp = self.generate_timestamp(single_date, i * (1440 // target_days))
                        reading = self.generate_sensor_reading(device_id, timestamp)
                        new_readings.append(reading)
                    
                    operations.append(UpdateOne(
                        {'_id': device_id},
                        {'$push': {'readings': {'$each': new_readings}}},
                        upsert=True
                    ))
                
                elif current_count < target_days:
                    # Need to add more readings
                    needed = target_days - current_count
                    print(f"Adding {needed} readings for {device_id} on {date_str}")
                    
                    # Get existing timestamps to avoid duplicates
                    existing_timestamps = set()
                    for reading in existing_readings:
                        ts_seconds = reading['timestamp']['_seconds']
                        existing_timestamps.add(ts_seconds)
                    
                    new_readings = []
                    attempts = 0
                    while len(new_readings) < needed and attempts < needed * 2:
                        random_minute = random.randint(0, 1439)
                        timestamp = self.generate_timestamp(single_date, random_minute)
                        
                        if timestamp['_seconds'] not in existing_timestamps:
                            reading = self.generate_sensor_reading(device_id, timestamp)
                            new_readings.append(reading)
                            existing_timestamps.add(timestamp['_seconds'])
                        
                        attempts += 1
                    
                    if new_readings:
                        operations.append(UpdateOne(
                            {'_id': device_id},
                            {'$push': {'readings': {'$each': new_readings}}}
                        ))
                
                elif current_count > target_days:
                    # Need to remove excess readings - keep well distributed ones
                    excess = current_count - target_days
                    print(f"Removing {excess} excess readings for {device_id} on {date_str}")
                    
                    # Sort readings by timestamp and select evenly distributed ones to keep
                    sorted_readings = sorted(existing_readings, 
                                           key=lambda x: x['timestamp']['_seconds'])
                    
                    # Calculate indices to keep (evenly distributed)
                    keep_indices = set()
                    for i in range(target_days):
                        idx = int(i * (current_count - 1) / (target_days - 1)) if target_days > 1 else 0
                        keep_indices.add(idx)
                    
                    # Identify readings to remove
                    readings_to_remove = []
                    for i, reading in enumerate(sorted_readings):
                        if i not in keep_indices:
                            readings_to_remove.append(reading)
                    
                    # Remove excess readings (keep only first 'excess' from to_remove list)
                    if readings_to_remove:
                        # We'll remove the first 'excess' readings from the to_remove list
                        remove_timestamps = [r['timestamp'] for r in readings_to_remove[:excess]]
                        
                        operations.append(UpdateOne(
                            {'_id': device_id},
                            {'$pull': {'readings': {'timestamp': {'$in': remove_timestamps}}}}
                        ))
        
        # Execute all operations
        if operations:
            print(f"Executing {len(operations)} operations for sensor readings")
            result = self.sensor_readings.bulk_write(operations, ordered=False)
            print(f"Sensor readings update result: {result.bulk_api_result}")
    
    def normalize_water_level_readings(self, target_days=200):
        """Normalize water level readings data"""
        start_date = datetime(2025, 9, 26)
        end_date = datetime(2025, 10, 31)
        
        print("Fetching water level readings data...")
        dates_data = self.iterative_fetch_dates(self.water_level_readings, start_date, end_date)
        
        for single_date in self.date_range(start_date, end_date):
            date_str = single_date.strftime('%Y-%m-%d')
            
            current_count = 0
            existing_readings = []
            
            if date_str in dates_data:
                current_count = dates_data[date_str]['count']
                existing_readings = dates_data[date_str]['readings']
            
            if current_count == 0:
                # No data for this date - generate full day
                print(f"Generating {target_days} water level readings for {date_str}")
                new_readings = []
                for i in range(target_days):
                    timestamp = self.generate_timestamp(single_date, i * (1440 // target_days))
                    reading = self.generate_water_level_reading(timestamp)
                    new_readings.append(reading)
                
                if new_readings:
                    self.water_level_readings.insert_many(new_readings)
            
            elif current_count < target_days:
                # Need to add more readings
                needed = target_days - current_count
                print(f"Adding {needed} water level readings for {date_str}")
                
                # Get existing timestamps to avoid duplicates
                existing_timestamps = set()
                for reading in existing_readings:
                    ts_seconds = reading['timestamp']['_seconds']
                    existing_timestamps.add(ts_seconds)
                
                new_readings = []
                attempts = 0
                while len(new_readings) < needed and attempts < needed * 2:
                    random_minute = random.randint(0, 1439)
                    timestamp = self.generate_timestamp(single_date, random_minute)
                    
                    if timestamp['_seconds'] not in existing_timestamps:
                        reading = self.generate_water_level_reading(timestamp)
                        new_readings.append(reading)
                        existing_timestamps.add(timestamp['_seconds'])
                    
                    attempts += 1
                
                if new_readings:
                    self.water_level_readings.insert_many(new_readings)
            
            elif current_count > target_days:
                # Need to remove excess readings
                excess = current_count - target_days
                print(f"Removing {excess} excess water level readings for {date_str}")
                
                # Sort readings by timestamp and select evenly distributed ones to keep
                sorted_readings = sorted(existing_readings, 
                                       key=lambda x: x['timestamp']['_seconds'])
                
                # Calculate indices to remove (remove excess from less distributed areas)
                remove_indices = []
                total_readings = len(sorted_readings)
                
                # Remove readings that are too close to each other
                timestamps = [r['timestamp']['_seconds'] for r in sorted_readings]
                time_differences = []
                
                for i in range(1, len(timestamps)):
                    time_differences.append((i, timestamps[i] - timestamps[i-1]))
                
                # Sort by smallest time differences (closest readings)
                time_differences.sort(key=lambda x: x[1])
                
                # Remove the readings with smallest time differences
                for i in range(min(excess, len(time_differences))):
                    remove_indices.append(time_differences[i][0])
                
                # Remove the identified readings
                if remove_indices:
                    readings_to_remove = [sorted_readings[i] for i in remove_indices]
                    remove_ids = [r['_id'] for r in readings_to_remove]
                    
                    self.water_level_readings.delete_many({'_id': {'$in': remove_ids}})
    
    def date_range(self, start_date, end_date):
        """Generator for date range"""
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)
    
    def run_normalization(self):
        """Run the complete normalization process"""
        print("Starting data normalization process...")
        
        try:
            # Normalize sensor readings
            self.normalize_sensor_readings()
            
            # Normalize water level readings
            self.normalize_water_level_readings()
            
            print("Data normalization completed successfully!")
            
        except Exception as e:
            print(f"Error during normalization: {str(e)}")
            raise
    
    def close(self):
        """Close database connection"""
        self.client.close()

# Usage
if __name__ == "__main__":
    # Update connection details if needed
    manager = MongoDBDataManager(host='localhost', port=27017)
    
    try:
        manager.run_normalization()
    finally:
        manager.close()