# app/utils/route_tester.py
import asyncio
import random
import httpx
from datetime import datetime
import signal
import sys

class SensorSimulator:
    def __init__(self):
        self.is_running = False
        self.current_task = None
    
    async def generate_random_sensor_data(self):
        """Generate random sensor data for testing"""
        # ESP32-1 (NPK Soil pH) - random values within realistic ranges
        npk_data = {
            "url": "/esp32-1",
            "data": {
                "nitrogen": round(random.uniform(20, 150), 1),
                "phosphorus": round(random.uniform(100, 200), 1),
                "potassium": round(random.uniform(100, 200), 1),
                "soilPh": round(random.uniform(5.5, 7.5), 1),
                "device_id": f"ESP32-NPKPH-{random.randint(1, 3)}"
            }
        }
        
        # ESP32-2 (Environmental) - random values within realistic ranges
        env_data = {
            "url": "/esp32-2",
            "data": {
                "soilMoisture": round(random.uniform(30, 100), 1),
                "temperature": round(random.uniform(20, 35), 1),
                "humidity": round(random.uniform(40, 90), 1),
                "device_id": f"ESP32-ENV-{random.randint(1, 3)}"
            }
        }
        
        # ESP32-3 (Water Level) - random values within realistic ranges
        water_data = {
            "url": "/esp32-3",
            "data": {
                "waterLevel": round(random.uniform(0, 100), 1),
                "device_id": f"ESP32-WATER-{random.randint(1, 3)}"
            }
        }
        
        return [npk_data, env_data, water_data]

    async def send_sensor_data(self, client, base_url, test_case):
        """Send sensor data to the API"""
        try:
            response = await client.post(
                f"{base_url}{test_case['url']}",
                json=test_case["data"],
                timeout=10.0
            )
            
            if response.status_code == 200:
                print(f"✅ {test_case['url']}: Success - {test_case['data']}")
            else:
                print(f"❌ {test_case['url']}: Failed - {response.status_code} {response.text}")
                
        except Exception as e:
            print(f"❌ {test_case['url']}: Error - {e}")

    async def continuous_sensor_testing(self):
        """Continuously send random sensor data every 3-5 seconds"""
        await asyncio.sleep(2)  # Wait for server to start
        
        base_url = "http://localhost:8000/api"
        iteration = 0
        
        print("🚀 Starting continuous sensor data simulation...")
        print("📊 Sending random sensor data every 3-5 seconds")
        print("⏸️  Press Ctrl+C to stop the simulation")
        print("-" * 50)
        
        self.is_running = True
        
        async with httpx.AsyncClient() as client:
            while self.is_running:
                try:
                    iteration += 1
                    print(f"\n🔄 Iteration {iteration} - {datetime.now().strftime('%H:%M:%S')}")
                    
                    # Generate new random data for each iteration
                    test_cases = await self.generate_random_sensor_data()
                    
                    # Send all sensor data
                    for test_case in test_cases:
                        await self.send_sensor_data(client, base_url, test_case)
                        await asyncio.sleep(0.2)  # Small delay between requests
                    
                    # Random delay between 3-5 seconds
                    delay = random.uniform(3, 5)
                    print(f"⏳ Next update in {delay:.1f} seconds...")
                    await asyncio.sleep(delay)
                    
                except asyncio.CancelledError:
                    print("🛑 Simulation cancelled")
                    break
                except Exception as e:
                    print(f"❌ Error in simulation: {e}")
                    await asyncio.sleep(5)  # Wait before retrying

    async def test_routes_on_startup(self):
        """Test all POST routes when the application starts (single run)"""
        await asyncio.sleep(2)  # Wait for server to start
        
        base_url = "http://localhost:8000/api"
        
        print("🧪 Testing POST routes with sample data...")
        
        test_cases = await self.generate_random_sensor_data()
        
        async with httpx.AsyncClient() as client:
            for test_case in test_cases:
                await self.send_sensor_data(client, base_url, test_case)
        
        print("✅ Initial route testing completed!")

    def stop(self):
        """Stop the continuous simulation"""
        self.is_running = False
        if self.current_task:
            self.current_task.cancel()

# Global instance
sensor_simulator = SensorSimulator()

def start_continuous_testing():
    """Start continuous sensor data testing in the background"""
    sensor_simulator.current_task = asyncio.create_task(sensor_simulator.continuous_sensor_testing())

def start_route_testing():
    """Start one-time route testing in the background"""
    asyncio.create_task(sensor_simulator.test_routes_on_startup())

def stop_testing():
    """Stop the continuous testing"""
    sensor_simulator.stop()

# For running directly
if __name__ == "__main__":
    async def main():
        print("🌱 Sensor Data Simulator")
        print("=" * 50)
        print("1. Continuous mode (runs forever)")
        print("2. Single test mode")
        
        choice = input("Choose mode (1 or 2): ").strip()
        
        # Setup signal handler for graceful shutdown
        def signal_handler(sig, frame):
            print("\n🛑 Received shutdown signal, stopping simulation...")
            sensor_simulator.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        if choice == "1":
            try:
                await sensor_simulator.continuous_sensor_testing()
            except KeyboardInterrupt:
                print("\n🛑 Simulation stopped by user")
        else:
            await sensor_simulator.test_routes_on_startup()
    
    asyncio.run(main())