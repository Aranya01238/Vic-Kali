"""
task_manager.py - Diya's Task & Assistant Capabilities

Reminders, to-do lists, scheduling, and quick productivity tools.
All data is persisted to tasks.json.
"""

import json
import os
import threading
import time
from datetime import datetime, timedelta


TASKS_FILE = "tasks.json"


def _load_tasks():
    """Load tasks from file."""
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        default = {
            "todos": [],
            "reminders": [],
            "schedule": [],
            "completed": [],
        }
        _save_tasks(default)
        return default


def _save_tasks(data):
    """Save tasks to file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ================= TO-DO LIST =================

def add_todo(task, priority="medium"):
    """Add a task to the to-do list."""
    data = _load_tasks()
    todo = {
        "id": len(data["todos"]) + len(data["completed"]) + 1,
        "task": task,
        "priority": priority,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "done": False,
    }
    data["todos"].append(todo)
    _save_tasks(data)
    return f"Added to-do #{todo['id']}: {task} (Priority: {priority})"


def complete_todo(task_id):
    """Mark a to-do item as complete."""
    data = _load_tasks()
    for i, todo in enumerate(data["todos"]):
        if todo["id"] == task_id:
            todo["done"] = True
            todo["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            data["completed"].append(data["todos"].pop(i))
            _save_tasks(data)
            return f"Completed: {todo['task']}"
    return f"Task #{task_id} not found."


def list_todos():
    """List all pending to-do items."""
    data = _load_tasks()
    todos = [t for t in data["todos"] if not t["done"]]

    if not todos:
        return "Your to-do list is empty! Nothing pending."

    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    todos.sort(key=lambda x: priority_order.get(x["priority"], 1))

    result = "Your To-Do List:\n\n"
    for t in todos:
        icon = {"high": "!!!", "medium": " ! ", "low": "   "}.get(t["priority"], " ! ")
        result += f"  [{icon}] #{t['id']}: {t['task']}\n"
        result += f"         Added: {t['created']}\n"

    result += f"\nTotal: {len(todos)} pending tasks"
    return result


def remove_todo(task_id):
    """Remove a to-do item."""
    data = _load_tasks()
    for i, todo in enumerate(data["todos"]):
        if todo["id"] == task_id:
            removed = data["todos"].pop(i)
            _save_tasks(data)
            return f"Removed: {removed['task']}"
    return f"Task #{task_id} not found."


# ================= REMINDERS =================

# Active reminder threads
_active_reminders = []


def add_reminder(message, minutes_from_now):
    """Set a reminder that fires after N minutes."""
    data = _load_tasks()
    fire_time = datetime.now() + timedelta(minutes=minutes_from_now)

    reminder = {
        "id": len(data["reminders"]) + 1,
        "message": message,
        "set_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "fire_at": fire_time.strftime("%Y-%m-%d %H:%M"),
        "fired": False,
    }
    data["reminders"].append(reminder)
    _save_tasks(data)

    # Start a background thread for this reminder
    def _fire_reminder():
        time.sleep(minutes_from_now * 60)
        print(f"\n[REMINDER] Diya: Hey! Reminder: {message}")
        # Mark as fired
        d = _load_tasks()
        for r in d["reminders"]:
            if r["id"] == reminder["id"]:
                r["fired"] = True
        _save_tasks(d)

    t = threading.Thread(target=_fire_reminder, daemon=True)
    t.start()
    _active_reminders.append(t)

    return f"Reminder set! I will remind you in {minutes_from_now} minutes: '{message}'"


def list_reminders():
    """List all active reminders."""
    data = _load_tasks()
    active = [r for r in data["reminders"] if not r["fired"]]

    if not active:
        return "No active reminders."

    result = "Active Reminders:\n\n"
    for r in active:
        result += f"  #{r['id']}: {r['message']}\n"
        result += f"         Fires at: {r['fire_at']}\n"

    return result


# ================= SCHEDULE =================

def add_schedule(event, day, time_str):
    """Add an event to the schedule."""
    data = _load_tasks()
    entry = {
        "id": len(data["schedule"]) + 1,
        "event": event,
        "day": day,
        "time": time_str,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    data["schedule"].append(entry)
    _save_tasks(data)
    return f"Scheduled: {event} on {day} at {time_str}"


def show_schedule():
    """Show the full schedule."""
    data = _load_tasks()
    sched = data["schedule"]

    if not sched:
        return "Your schedule is empty."

    result = "Your Schedule:\n\n"
    for s in sched:
        result += f"  #{s['id']}: {s['event']}\n"
        result += f"         {s['day']} at {s['time']}\n"

    return result


# ================= INTENT DETECTION =================

def detect_task_intent(text):
    """Detect if the user wants to do a task management action."""
    t = text.lower()

    # Add to-do
    if any(p in t for p in ["add task", "add a task", "add to-do", "add a to-do", "add todo", "add a todo", "new task"]):
        task = text.split(":", 1)[-1].strip() if ":" in text else text.replace("add task", "").replace("add a task", "").replace("add to-do", "").replace("add a to-do", "").replace("add todo", "").replace("add a todo", "").replace("new task", "").strip()
        priority = "high" if "urgent" in t or "important" in t else "medium"
        if task:
            return ("add_todo", {"task": task, "priority": priority})

    # Complete to-do
    if any(p in t for p in ["complete task", "done task", "finish task", "mark done"]):
        import re
        m = re.search(r'#?(\d+)', text)
        if m:
            return ("complete_todo", {"task_id": int(m.group(1))})

    # List to-dos
    if any(p in t for p in ["show tasks", "list tasks", "my tasks", "to-do list", "todo list", "what's on my list", "pending tasks"]):
        return ("list_todos", {})

    # Remove to-do
    if any(p in t for p in ["remove task", "delete task"]):
        import re
        m = re.search(r'#?(\d+)', text)
        if m:
            return ("remove_todo", {"task_id": int(m.group(1))})

    # Set reminder
    if any(p in t for p in ["remind me", "set reminder", "set a reminder"]):
        import re
        # Try to extract minutes
        m = re.search(r'in\s+(\d+)\s*(min|minute|minutes|hour|hours)', t)
        minutes = 30  # default
        if m:
            val = int(m.group(1))
            unit = m.group(2)
            if "hour" in unit:
                minutes = val * 60
            else:
                minutes = val

        msg = text
        for prefix in ["remind me to", "remind me", "set reminder", "set a reminder"]:
            if prefix in t:
                msg = text[t.index(prefix) + len(prefix):].strip()
                # Remove the time part
                msg = re.sub(r'in\s+\d+\s*(min|minute|minutes|hour|hours)', '', msg).strip()
                break

        if msg:
            return ("add_reminder", {"message": msg, "minutes_from_now": minutes})

    # List reminders
    if any(p in t for p in ["show reminders", "list reminders", "my reminders"]):
        return ("list_reminders", {})

    # Schedule - ADD entry
    if any(p in t for p in ["schedule", "add to schedule", "schedule a", "schedule the", "schedule me"]):
        # Check if this is a query (show schedule) vs adding
        if any(p in t for p in ["show", "list", "what", "when", "tell me"]):
            return ("show_schedule", {})
        
        # Parse time pattern: "at 5:15", "at 5", "at 5pm", "at 5:00 p.m."
        import re
        time_pattern = r'at\s+(\d{1,2})(?::?(\d{2}))?\s*(?:a\.?m\.?|p\.?m\.?)?'
        time_match = re.search(time_pattern, t, re.IGNORECASE)
        
        if time_match:
            hour = time_match.group(1)
            minute = time_match.group(2) or "00"
            time_str = f"{hour}:{minute}"
            
            # Extract event name (everything before "at time")
            event = text[:time_match.start()].strip()
            for prefix in ["schedule", "add to schedule", "schedule a", "schedule me", "schedule the"]:
                if event.lower().startswith(prefix):
                    event = event[len(prefix):].strip()
                    break
            
            if event:
                # Determine day (default to today)
                day = "today"
                day_pattern = r'(today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)'
                day_match = re.search(day_pattern, t, re.IGNORECASE)
                if day_match:
                    day = day_match.group(1).lower()
                
                return ("add_schedule", {"event": event, "day": day, "time_str": time_str})
        
        # Fallback: show schedule if no time detected
        return ("show_schedule", {})

    return None


def execute_task_action(action, args):
    """Execute a task management action."""
    actions = {
        "add_todo": add_todo,
        "complete_todo": complete_todo,
        "list_todos": list_todos,
        "remove_todo": remove_todo,
        "add_reminder": add_reminder,
        "list_reminders": list_reminders,
        "add_schedule": add_schedule,
        "show_schedule": show_schedule,
    }

    fn = actions.get(action)
    if fn:
        return fn(**args)
    return None
