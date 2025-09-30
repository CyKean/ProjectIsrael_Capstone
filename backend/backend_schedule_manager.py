import asyncio
import time
import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple
import threading
from dataclasses import dataclass
import json

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [BackendScheduler] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

@dataclass
class Schedule:
    id: str
    mode: str  # 'one-time', 'daily', 'weekly'
    scheduled_time: int  # timestamp in milliseconds
    duration: int  # in minutes
    days: Optional[Dict] = None  # for weekly schedules
    days_array: Optional[List[int]] = None  # for weekly schedules
    notify_watering: bool = True
    completed: bool = False
    water_flow_rate: str = 'medium'
    skip_if_rain: bool = False

class BackendScheduleManager:
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url
        self.schedules_cache: List[Schedule] = []
        self.active_schedules: Dict[str, Dict] = {}
        self.schedule_timers: Dict[str, threading.Timer] = {}
        self.executed_schedules_today: Set[str] = set()
        self.schedule_execution_states: Dict[str, str] = {}
        self.is_running = False
        self.check_interval = 0.5  # seconds
        
        # Heartbeat tracking
        self.heartbeat_timeout = 30  # seconds without heartbeat = frontend dead
        
        # Motor control locks to prevent duplicates
        self.motor_control_locks: Set[str] = set()
        self.last_motor_commands: Dict[str, float] = {}
        
        # New tracking systems from Sidebar.vue
        self.processing_schedules: Set[str] = set()
        self.last_toast_messages: Dict[str, float] = {}
        self.last_watering_notifications: Dict[str, float] = {}
        self.last_history_saves: Dict[str, float] = {}
        self.schedule_execution_locks: Dict[str, float] = {}
        
        # Event loop for async operations in threads
        self._loop = None
        
        print("🟢 [INIT] Backend Schedule Manager initialized")
        print(f"🟢 [CONFIG] API Base URL: {api_base_url}")
        print(f"🟢 [CONFIG] Heartbeat Timeout: {self.heartbeat_timeout}s")
        print(f"🟢 [CONFIG] Check Interval: {self.check_interval}s")

    def _run_async_in_thread(self, coro):
        """Run async coroutine in a thread-safe way"""
        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(coro, self._loop)
        else:
            print("❌ [ASYNC] No running event loop available")

    async def check_frontend_heartbeat(self) -> bool:
        """
        Check if frontend is active by looking for recent heartbeat
        """
        try:
            response = requests.get(
                f"{self.api_base_url}/system/heartbeat",
                timeout=5
            )
            
            if response.status_code == 200:
                heartbeat_data = response.json()
                last_seen_str = heartbeat_data.get('last_seen')
                
                if last_seen_str:
                    # Parse the timestamp
                    if last_seen_str.endswith('Z'):
                        last_seen_str = last_seen_str[:-1] + '+00:00'
                    
                    last_seen_time = datetime.fromisoformat(last_seen_str)
                    current_time = datetime.now(last_seen_time.tzinfo) if last_seen_time.tzinfo else datetime.now()
                    
                    time_diff = (current_time - last_seen_time).total_seconds()
                    
                    if time_diff < self.heartbeat_timeout:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
            
        except Exception as e:
            return False

    async def is_frontend_active(self) -> bool:
        """
        Determine if frontend is actively running and managing schedules
        """
        result = await self.check_frontend_heartbeat()
        return result

    async def fetch_active_schedules(self) -> List[Schedule]:
        """
        Fetch active schedules from the backend API
        """
        try:
            response = requests.get(f"{self.api_base_url}/schedules/active", timeout=10)
            if response.status_code == 200:
                schedules_data = response.json()
                print(f"📦 [SCHEDULES] Fetched {len(schedules_data)} schedules from API")
                parsed_schedules = self._parse_schedules(schedules_data)
                return parsed_schedules
            else:
                print(f"❌ [SCHEDULES] API returned status code: {response.status_code}")
        except Exception as e:
            print(f"❌ [SCHEDULES] Error fetching schedules: {e}")
        return []

    def _parse_schedules(self, schedules_data: List[Dict]) -> List[Schedule]:
        """
        Parse schedule data from API response
        """
        schedules = []
        for data in schedules_data:
            try:
                # Convert days object to array for weekly schedules
                days_array = None
                if data.get('mode') == 'weekly' and data.get('days'):
                    days_array = self._convert_days_format(data['days'])
                
                schedule = Schedule(
                    id=str(data['id']),
                    mode=data['mode'],
                    scheduled_time=data['scheduledTime'],
                    duration=data['duration'],
                    days=data.get('days'),
                    days_array=days_array,
                    notify_watering=data.get('notifyWatering', True),
                    completed=data.get('completed', False),
                    water_flow_rate=data.get('waterFlowRate', 'medium'),
                    skip_if_rain=data.get('skipIfRain', False)
                )
                schedules.append(schedule)
                print(f"  ✅ [SCHEDULE] ID: {schedule.id}, Mode: {schedule.mode}, Time: {schedule.scheduled_time}")
            except KeyError as e:
                print(f"⚠️ [SCHEDULES] Invalid schedule data missing key {e}: {data}")
            except Exception as e:
                print(f"❌ [SCHEDULES] Error parsing schedule: {e}, Data: {data}")
        return schedules

    def _convert_days_format(self, days_object) -> List:
        """
        Convert days object to array format - handles both dict and list inputs
        """
        if isinstance(days_object, dict):
            # Handle dictionary format: {"0": true, "1": false, ...}
            result = [int(key) for key, value in days_object.items() if value is True]
            return result
        elif isinstance(days_object, list):
            # Handle array format - could be boolean [True, False, True] or index [0, 2, 4]
            if len(days_object) > 0 and isinstance(days_object[0], bool):
                # Boolean array - convert to index array for consistency
                result = [i for i, day_enabled in enumerate(days_object) if day_enabled is True]
                return result
            else:
                # Already index array format
                return days_object
        else:
            return []

    def should_skip_schedule(self, schedule: Schedule, schedule_key: str, now: datetime) -> bool:
        """
        Check if a schedule should be skipped
        """
        today = now.strftime('%Y-%m-%d')
        execution_key = f"{schedule.id}-{today}"
        
        # Skip if already executed today
        if execution_key in self.executed_schedules_today:
            return True
            
        # Skip if already active
        if schedule.id in self.active_schedules:
            return True
            
        # Skip if execution is in progress
        if self.schedule_execution_states.get(execution_key) == 'executing':
            return True
            
        # Skip if processing
        if schedule_key in self.processing_schedules:
            return True
            
        return False

    async def check_one_time_schedules(self, now: datetime, current_day: int):
        """
        Check and execute one-time schedules
        """
        one_time_schedules = [
            s for s in self.schedules_cache 
            if s.mode == 'one-time' and s.notify_watering and not s.completed
        ]
        
        if one_time_schedules:
            print(f"🔍 [ONE-TIME] Checking {len(one_time_schedules)} one-time schedules")
        
        for schedule in one_time_schedules:
            schedule_key = f"{schedule.id}-{current_day}"
            
            if self.should_skip_schedule(schedule, schedule_key, now):
                continue
                
            # For one-time schedules, check if the scheduled date/time matches current date/time
            schedule_datetime = datetime.fromtimestamp(schedule.scheduled_time / 1000)
            current_datetime = now
            
            # Check if it's the same day and time is within 1 second tolerance
            same_day = schedule_datetime.date() == current_datetime.date()
            time_diff_ms = abs(current_datetime.timestamp() * 1000 - schedule.scheduled_time)
            time_match = time_diff_ms < 1000  # 1 second tolerance
            
            if same_day and time_match:
                print(f"🚀 [ONE-TIME] EXECUTING schedule {schedule.id} at {now.strftime('%H:%M:%S')}")
                await self.start_schedule_execution(schedule, current_day, now)

    async def check_daily_schedules(self, now: datetime, current_day: int):
        """
        Check and execute daily schedules
        """
        daily_schedules = [
            s for s in self.schedules_cache 
            if s.mode == 'daily' and s.notify_watering and not s.completed
        ]
        
        if daily_schedules:
            print(f"🔍 [DAILY] Checking {len(daily_schedules)} daily schedules")
        
        current_time_ms = (now.hour * 3600 + now.minute * 60 + now.second) * 1000
        
        for schedule in daily_schedules:
            schedule_key = f"{schedule.id}-{current_day}"
            
            if self.should_skip_schedule(schedule, schedule_key, now):
                continue
                
            # For daily schedules, just check if the time matches (runs every day)
            time_match = abs(current_time_ms - schedule.scheduled_time) < 1000  # 1 second tolerance
            
            if time_match:
                print(f"🚀 [DAILY] EXECUTING schedule {schedule.id} at {now.strftime('%H:%M:%S')}")
                await self.start_schedule_execution(schedule, current_day, now)

    async def check_weekly_schedules(self, now: datetime, current_day: int):
        """
        Check and execute weekly schedules - UPDATED with proper next day focus
        """
        weekly_schedules = [
            s for s in self.schedules_cache 
            if s.mode == 'weekly' and s.notify_watering and not s.completed
        ]
        
        if weekly_schedules:
            print(f"🔍 [WEEKLY] Checking {len(weekly_schedules)} weekly schedules")
            print(f"   📅 Today is day {current_day} ({self.get_day_name(current_day)})")
        
        current_time_ms = (now.hour * 3600 + now.minute * 60 + now.second) * 1000
        
        for schedule in weekly_schedules:
            schedule_key = f"{schedule.id}-{current_day}"
            
            if self.should_skip_schedule(schedule, schedule_key, now):
                continue
            
            # For weekly schedules, check if current day is in schedule's days AND time matches
            should_run = False
            
            # Use days_array which should contain day indices [0, 2, 4] for enabled days
            if schedule.days_array and isinstance(schedule.days_array, list):
                should_run = current_day in schedule.days_array
                enabled_days_names = [self.get_day_name(day) for day in schedule.days_array]
                print(f"   📅 Schedule {schedule.id} runs on: {schedule.days_array} ({', '.join(enabled_days_names)})")
                print(f"   📅 Day {current_day} ({self.get_day_name(current_day)}) in schedule: {should_run}")
                    
            time_match = abs(current_time_ms - schedule.scheduled_time) < 1000  # 1 second tolerance
            
            # Convert times for better readability
            current_time_str = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
            scheduled_time_str = self._ms_to_time_string(schedule.scheduled_time)
            time_diff = abs(current_time_ms - schedule.scheduled_time)
            
            print(f"   ⏰ Current: {current_time_str}, Scheduled: {scheduled_time_str}, Diff: {time_diff}ms")
            print(f"   ⏰ Time match: {time_match}")
            
            if should_run and time_match:
                print(f"🚀 [WEEKLY] EXECUTING schedule {schedule.id} on {self.get_day_name(current_day)} at {now.strftime('%H:%M:%S')}")
                await self.start_schedule_execution(schedule, current_day, now)
            else:
                # Calculate next execution time - NEW IMPROVED LOGIC
                next_execution_info = self._get_next_weekly_execution(schedule, current_day, current_time_ms)
                if next_execution_info:
                    next_day, next_day_name, days_until, time_until_str = next_execution_info
                    print(f"   📅 Next execution: {next_day_name} at {scheduled_time_str} (in {days_until} days, {time_until_str})")
                else:
                    print(f"   📅 No upcoming executions found for schedule {schedule.id}")

    def _get_next_weekly_execution(self, schedule: Schedule, current_day: int, current_time_ms: int) -> Optional[Tuple[int, str, int, str]]:
        """
        Calculate the next execution time for a weekly schedule
        Returns: (next_day, next_day_name, days_until, time_until_str)
        """
        if not schedule.days_array:
            return None
        
        scheduled_time_str = self._ms_to_time_string(schedule.scheduled_time)
        
        # Check if today is in schedule but time hasn't come yet
        if current_day in schedule.days_array and current_time_ms < schedule.scheduled_time:
            # Today, but scheduled time is in the future
            seconds_until = (schedule.scheduled_time - current_time_ms) // 1000
            hours = seconds_until // 3600
            minutes = (seconds_until % 3600) // 60
            time_until_str = f"{hours:02d}:{minutes:02d}:{seconds_until % 60:02d}"
            return (current_day, self.get_day_name(current_day), 0, time_until_str)
        
        # Find the next scheduled day in the current week
        next_days_current_week = [day for day in schedule.days_array if day > current_day]
        
        if next_days_current_week:
            # There are scheduled days later in the current week
            next_day = min(next_days_current_week)
            days_until = next_day - current_day
            next_day_name = self.get_day_name(next_day)
            time_until_str = "at scheduled time"
            
            return (next_day, next_day_name, days_until, time_until_str)
        
        else:
            # No more days this week - wrap to next week
            next_day = min(schedule.days_array)
            days_until = (7 - current_day) + next_day
            next_day_name = self.get_day_name(next_day)
            time_until_str = "at scheduled time"
            
            return (next_day, next_day_name, days_until, time_until_str)

    def _ms_to_time_string(self, ms_time: int) -> str:
        """Convert milliseconds since midnight to time string"""
        total_seconds = ms_time // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    async def start_schedule_execution(self, schedule: Schedule, current_day: int, now: datetime):
        """
        Start schedule execution atomically
        """
        schedule_id = schedule.id
        today = now.strftime('%Y-%m-%d')
        execution_key = f"{schedule_id}-{today}"
        
        print(f"⚡ [ATOMIC_START] Starting {schedule.mode} schedule {schedule_id}")
        
        # Check if already executed today
        if execution_key in self.executed_schedules_today:
            print(f"⏩ [ATOMIC_START] Schedule {schedule_id} already executed today - SKIPPING")
            return
            
        # Check if execution is in progress
        if self.schedule_execution_states.get(execution_key) == 'executing':
            print(f"⏩ [ATOMIC_START] Schedule {schedule_id} execution in progress - SKIPPING")
            return
            
        # Set execution state
        self.schedule_execution_states[execution_key] = 'executing'
        self.executed_schedules_today.add(execution_key)
        
        try:
            await self.execute_complete_schedule_process(schedule, current_day, now)
            print(f"✅ [ATOMIC_START] Atomic execution completed for schedule {schedule_id}")
        except Exception as e:
            print(f"❌ [ATOMIC_START] Atomic execution failed for schedule {schedule_id}: {e}")
            # Reset execution state on error
            self.schedule_execution_states.pop(execution_key, None)
            self.executed_schedules_today.discard(execution_key)

    async def execute_complete_schedule_process(self, schedule: Schedule, current_day: int, now: datetime):
        """
        Execute the complete schedule process
        """
        schedule_id = schedule.id
        start_time = int(time.time() * 1000)
        
        print(f"🔄 [COMPLETE_PROCESS] Executing {schedule.mode} schedule {schedule_id}")
        
        # STEP 1: Save start notification
        await self.save_schedule_start_notification(schedule, now)
        
        # STEP 2: Change motor status to ON
        await self.change_motor_status_to_on(schedule_id)
        
        # STEP 3: Set timer for end
        self.set_schedule_end_timer(schedule, current_day, start_time)
        
        print(f"✅ [COMPLETE_PROCESS] Complete process started for schedule {schedule_id}")

    async def save_schedule_start_notification(self, schedule: Schedule, now: datetime, current_day: Optional[int] = None):
        """
        Save schedule start notification - FIXED: made current_day optional
        """
        schedule_id = schedule.id
        notification_key = f"backend-start-{schedule_id}-{now.strftime('%Y-%m-%d')}"
        
        formatted_time = now.strftime('%a, %b %d, %I:%M:%S %p')
        
        if schedule.mode == 'one-time':
            title = 'One-time Watering Started (Backend)'
            message = f"One-time watering started at {formatted_time}"
        elif schedule.mode == 'daily':
            title = 'Daily Watering Started (Backend)'
            message = f"Daily watering started at {formatted_time}"
        elif schedule.mode == 'weekly':
            # Use current_day if provided, otherwise calculate from now
            day_num = current_day if current_day is not None else (now.weekday() + 6) % 7
            day_name = self.get_day_name(day_num)
            title = 'Weekly Watering Started (Backend)'
            message = f"Weekly watering ({day_name}) started at {formatted_time}"
        else:
            title = 'Scheduled Watering Started (Backend)'
            message = f"Watering started at {formatted_time}"
        
        print(f"   📢 [NOTIFICATION] {message}")
        
        try:
            success = await self.send_notification(message, title, 'info', notification_key)
            if success:
                print(f"   ✅ [NOTIFICATION] Start notification saved for {schedule_id}")
        except Exception as e:
            print(f"   ❌ [NOTIFICATION] Error saving start notification for {schedule_id}: {e}")

    async def change_motor_status_to_on(self, schedule_id: str):
        """
        Change motor status to ON
        """
        motor_key = f"backend-motor-on-{schedule_id}-{datetime.now().strftime('%Y-%m-%d')}"
        
        # Check if already changed today
        if motor_key in self.last_motor_commands:
            last_sent = self.last_motor_commands[motor_key]
            if time.time() - last_sent < 120:  # 2-minute cooldown
                print(f"   ⏩ [MOTOR] Motor already turned ON today for {schedule_id}")
                return
                
        if motor_key in self.motor_control_locks:
            print(f"   ⏩ [MOTOR] Motor command already in progress: {motor_key}")
            return
            
        self.motor_control_locks.add(motor_key)
        self.last_motor_commands[motor_key] = time.time()
        
        try:
            print(f"   ⚡ [MOTOR] Turning motor ON for schedule {schedule_id}")
            success = await self.update_motor_status(True, schedule_id, 'backend-schedule-start')
            
            if success:
                print(f"   ✅ [MOTOR] Motor turned ON successfully for {schedule_id}")
            else:
                print(f"   ❌ [MOTOR] Failed to turn motor ON for {schedule_id}")
                
        except Exception as e:
            print(f"   ❌ [MOTOR] Error turning motor ON for {schedule_id}: {e}")
        finally:
            # Release lock after a delay
            threading.Timer(10, lambda: self.motor_control_locks.discard(motor_key)).start()

    def set_schedule_end_timer(self, schedule: Schedule, current_day: int, start_time: int):
        """
        Set timer for schedule end - FIXED to handle async properly
        """
        schedule_id = schedule.id
        
        # Clear any existing timer
        if schedule_id in self.schedule_timers:
            self.schedule_timers[schedule_id].cancel()
        
        # Set new timer
        timer_duration = max(schedule.duration * 60 - 0.1, 1)  # Convert to seconds
        
        print(f"   ⏰ [TIMER] Timer set for {schedule_id} - will end in {schedule.duration} minutes")
        
        # Create a thread-safe timer that uses the event loop
        timer = threading.Timer(timer_duration, self._execute_schedule_end_safe, [schedule, current_day, start_time])
        
        self.schedule_timers[schedule_id] = timer
        timer.start()

    def _execute_schedule_end_safe(self, schedule: Schedule, current_day: int, start_time: int):
        """
        Thread-safe method to execute schedule end process
        """
        # Use the async runner to execute the async coroutine
        self._run_async_in_thread(self.execute_schedule_end_process(schedule, current_day, start_time))

    async def execute_schedule_end_process(self, schedule: Schedule, current_day: int, start_time: int):
        """
        Execute schedule end process
        """
        schedule_id = schedule.id
        today = datetime.now().strftime('%Y-%m-%d')
        execution_key = f"{schedule_id}-{today}"
        
        print(f"🛑 [END_PROCESS] Ending {schedule.mode} schedule {schedule_id}")
        
        try:
            # Save end notification
            await self.save_schedule_end_notification(schedule)
            
            # Change motor status to OFF
            await self.change_motor_status_to_off(schedule_id)
            
            # Save schedule to history
            await self.save_schedule_to_history(schedule, start_time, current_day)
            
            # Handle mode-specific completion
            await self.handle_schedule_completion(schedule, current_day)
            
            print(f"✅ [END_PROCESS] End process completed for schedule {schedule_id}")
            
        except Exception as e:
            print(f"❌ [END_PROCESS] End process failed for schedule {schedule_id}: {e}")
        finally:
            # Clean up
            self.active_schedules.pop(schedule_id, None)
            self.schedule_timers.pop(schedule_id, None)
            self.schedule_execution_states.pop(execution_key, None)

    async def save_schedule_end_notification(self, schedule: Schedule):
        """
        Save schedule end notification
        """
        schedule_id = schedule.id
        notification_key = f"backend-end-{schedule_id}-{datetime.now().strftime('%Y-%m-%d')}"
        
        now = datetime.now()
        formatted_time = now.strftime('%a, %b %d, %I:%M:%S %p')
        
        if schedule.mode == 'one-time':
            title = 'One-time Watering Completed (Backend)'
            message = f"One-time watering completed at {formatted_time}"
        elif schedule.mode == 'daily':
            title = 'Daily Watering Completed (Backend)'
            message = f"Daily watering completed at {formatted_time}"
        elif schedule.mode == 'weekly':
            day_name = self.get_day_name((now.weekday() + 6) % 7)
            title = 'Weekly Watering Completed (Backend)'
            message = f"Weekly watering ({day_name}) completed at {formatted_time}"
        else:
            title = 'Scheduled Watering Completed (Backend)'
            message = f"Watering completed at {formatted_time}"
        
        print(f"   📢 [NOTIFICATION] {message}")
        
        try:
            success = await self.send_notification(message, title, 'success', notification_key)
            if success:
                print(f"   ✅ [NOTIFICATION] End notification saved for {schedule_id}")
        except Exception as e:
            print(f"   ❌ [NOTIFICATION] Error saving end notification for {schedule_id}: {e}")

    async def change_motor_status_to_off(self, schedule_id: str):
        """
        Change motor status to OFF
        """
        motor_key = f"backend-motor-off-{schedule_id}-{datetime.now().strftime('%Y-%m-%d')}"
        
        # Check if already changed today
        if motor_key in self.last_motor_commands:
            last_sent = self.last_motor_commands[motor_key]
            if time.time() - last_sent < 120:  # 2-minute cooldown
                print(f"   ⏩ [MOTOR] Motor already turned OFF today for {schedule_id}")
                return
                
        if motor_key in self.motor_control_locks:
            print(f"   ⏩ [MOTOR] Motor command already in progress: {motor_key}")
            return
            
        self.motor_control_locks.add(motor_key)
        self.last_motor_commands[motor_key] = time.time()
        
        try:
            print(f"   ⚡ [MOTOR] Turning motor OFF for schedule {schedule_id}")
            success = await self.update_motor_status(False, schedule_id, 'backend-schedule-end')
            
            if success:
                print(f"   ✅ [MOTOR] Motor turned OFF successfully for {schedule_id}")
            else:
                print(f"   ❌ [MOTOR] Failed to turn motor OFF for {schedule_id}")
                
        except Exception as e:
            print(f"   ❌ [MOTOR] Error turning motor OFF for {schedule_id}: {e}")
        finally:
            # Release lock after a delay
            threading.Timer(10, lambda: self.motor_control_locks.discard(motor_key)).start()

    async def update_motor_status(self, status: bool, schedule_id: str, action_type: str) -> bool:
        """
        Update motor status via API
        """
        try:
            response = requests.post(
                f"{self.api_base_url}/motor-status-ph",
                json={
                    "status": status,
                    "source": f"backend-schedule-{schedule_id}-{action_type}",
                    "device_id": "main_motor"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('message') or result.get('status') == 'success':
                    return True
                    
            print(f"   ❌ [MOTOR_API] Motor control returned non-success status: {response.status_code}")
            return False
            
        except Exception as e:
            print(f"   ❌ [MOTOR_API] Motor control failed: {e}")
            return False

    async def send_notification(self, message: str, title: str, severity: str, unique_key: str, context_data: Dict = None) -> bool:
        """
        Send notification via API
        """
        try:
            payload = {
                "message": message,
                "title": title,
                "severity": severity,
                "uniqueKey": unique_key,
                "contextData": context_data or {
                    "type": "watering-schedule",
                    "source": "backend-scheduler",
                    "timestamp": datetime.now().isoformat()
                },
                "type": "system"
            }
            
            response = requests.post(
                f"{self.api_base_url}/notifications",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return True
            else:
                print(f"   ❌ [NOTIFICATION_API] Notification send failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ [NOTIFICATION_API] Error sending notification: {e}")
            return False

    async def save_schedule_to_history(self, schedule: Schedule, start_time: int, day: int) -> bool:
        """
        Save schedule to history
        """
        try:
            end_timestamp = int(time.time() * 1000)
            
            # Fixed ternary operator - Python uses if/else instead of ?:
            day_of_week = day if schedule.mode == 'weekly' else None
            
            history_data = {
                "scheduleId": schedule.id,
                "mode": schedule.mode,
                "originalScheduledTime": schedule.scheduled_time,
                "actualStartTime": start_time,
                "completedAt": end_timestamp,
                "duration": schedule.duration,
                "days": schedule.days or {},
                "dayOfWeek": day_of_week,
                "notifyWatering": schedule.notify_watering,
                "skipIfRain": schedule.skip_if_rain,
                "waterFlowRate": schedule.water_flow_rate,
                "status": "completed",
                "source": "backend-scheduler"
            }
            
            response = requests.post(
                f"{self.api_base_url}/schedules/history",
                json=history_data,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"   ✅ [HISTORY] Schedule history saved for {schedule.id}")
                return True
            else:
                print(f"   ❌ [HISTORY] History save failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ [HISTORY] Error saving schedule history: {e}")
            return False

    async def handle_schedule_completion(self, schedule: Schedule, current_day: int):
        """
        Handle schedule completion based on mode
        """
        schedule_id = schedule.id
        
        if schedule.mode == 'one-time':
            print(f"   📝 [COMPLETION] Marking one-time schedule {schedule_id} as completed")
            success = await self.mark_schedule_completed(schedule_id)
            if success:
                print(f"   ✅ [COMPLETION] One-time schedule {schedule_id} marked as completed")
            else:
                print(f"   ❌ [COMPLETION] Failed to mark one-time schedule {schedule_id} as completed")
                
        elif schedule.mode == 'daily':
            print(f"   🔄 [COMPLETION] Daily schedule {schedule_id} completed - will run again tomorrow")
            # Daily schedules automatically run again
            
        elif schedule.mode == 'weekly':
            print(f"   📅 [COMPLETION] Weekly schedule {schedule_id} completed for {self.get_day_name(current_day)} - focusing on next scheduled day")
            # Weekly schedules continue with next scheduled day automatically

    async def mark_schedule_completed(self, schedule_id: str) -> bool:
        """
        Mark schedule as completed via API
        """
        try:
            response = requests.put(
                f"{self.api_base_url}/schedules/{schedule_id}/complete",
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success' or result.get('schedule_type'):
                    print(f"   ✅ [COMPLETION_API] Schedule {schedule_id} marked as completed")
                    return True
                    
            print(f"   ❌ [COMPLETION_API] Schedule completion returned non-success: {response.status_code}")
            return False
            
        except Exception as e:
            print(f"   ❌ [COMPLETION_API] Error marking schedule as completed: {e}")
            return False

    def get_day_name(self, day_number: int) -> str:
        """
        Get day name from day number (Monday=0, Sunday=6)
        """
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return day_names[day_number] if 0 <= day_number < len(day_names) else 'Unknown'

    async def check_schedules(self):
        """
        Main function to check all schedules - IMPROVED CLEANUP LOGIC
        """
        try:
            now = datetime.now()
            # Python: Monday=0, Sunday=6 - this matches your expected format
            current_day = now.weekday()
            
            print(f"📅 [DEBUG] Today is: {self.get_day_name(current_day)} (Day {current_day})")
            
            # IMPROVED CLEANUP LOGIC - Remove all old execution tracking
            today = now.strftime('%Y-%m-%d')
            
            # Remove ALL old execution tracking (not just yesterday)
            self.executed_schedules_today = {
                key for key in self.executed_schedules_today 
                if key.endswith(today)  # Keep only today's entries
            }
            
            self.schedule_execution_states = {
                k: v for k, v in self.schedule_execution_states.items() 
                if k.endswith(today)  # Keep only today's entries
            }
            
            # Get schedule stats
            one_time_count = len([s for s in self.schedules_cache if s.mode == 'one-time' and not s.completed])
            daily_count = len([s for s in self.schedules_cache if s.mode == 'daily' and not s.completed])
            weekly_count = len([s for s in self.schedules_cache if s.mode == 'weekly' and not s.completed])
            
            if one_time_count > 0 or daily_count > 0 or weekly_count > 0:
                print(f"📊 [STATS] Active schedules: {one_time_count} one-time, {daily_count} daily, {weekly_count} weekly")
            
            # Check each schedule type
            await self.check_one_time_schedules(now, current_day)
            await self.check_daily_schedules(now, current_day)
            await self.check_weekly_schedules(now, current_day)
            
        except Exception as e:
            print(f"❌ [CHECK] Schedule check error: {e}")

    async def start(self):
        """
        Start the backend schedule manager
        """
        if self.is_running:
            print("⚠️ [START] Backend Schedule Manager is already running")
            return
            
        self.is_running = True
        print("🚀 [START] Starting Backend Schedule Manager")
        
        def run_loop():
            print("🔄 [MAIN_LOOP] Starting main loop in separate thread")
            # Store the event loop for thread-safe async operations
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            try:
                self._loop.run_until_complete(self._main_loop())
            except Exception as e:
                print(f"❌ [MAIN_LOOP] Error in main loop: {e}")
            finally:
                self._loop.close()
                self._loop = None
    
        # Run in a separate thread to avoid blocking
        self.thread = threading.Thread(target=run_loop, daemon=True)
        self.thread.start()
        print("✅ [START] Backend Schedule Manager started successfully")

    async def _main_loop(self):
        """
        Main loop for schedule checking
        """
        loop_count = 0
        print("🔄 [MAIN_LOOP] Entering main loop")
        
        while self.is_running:
            try:
                loop_count += 1
                
                # Refresh schedules every 60 checks (about 30 seconds)
                if loop_count % 60 == 0:
                    print("🔄 [MAIN_LOOP] Refreshing schedules cache...")
                    self.schedules_cache = await self.fetch_active_schedules()
                
                # Check if frontend is active
                frontend_active = await self.is_frontend_active()
                
                if not frontend_active:
                    # Frontend is not active - backend takes over
                    await self.check_schedules()
                else:
                    # Frontend is active - backend stays passive
                    if loop_count % 120 == 0:  # Print status every minute when passive
                        print("🟡 [MAIN_LOOP] Frontend active - backend in standby mode")
                
                await asyncio.sleep(self.check_interval)
                
            except Exception as e:
                print(f"❌ [MAIN_LOOP] Error in main loop: {e}")
                await asyncio.sleep(1)  # Wait a bit before retrying

    def stop(self):
        """
        Stop the backend schedule manager
        """
        self.is_running = False
        print("🛑 [STOP] Stopping Backend Schedule Manager")
        
        # Cancel all active timers
        timer_count = len(self.schedule_timers)
        for timer in self.schedule_timers.values():
            timer.cancel()
        self.schedule_timers.clear()
        
        print(f"✅ [STOP] Backend Schedule Manager stopped - Cancelled {timer_count} timers")

# Global instance
backend_scheduler = BackendScheduleManager(api_base_url="http://localhost:8000/api")