"""
second_brain.py - Diya as Your External Brain/Memory System

Extends Diya into a comprehensive knowledge capture, organization, and recall system.
Features:
- Smart note-taking with automatic tagging
- Knowledge base organization by topic
- Daily insights and learning logs
- Habit and project tracking
- Quick recall and search
- Periodic reviews and summaries
"""

import json
import os
from datetime import datetime, timedelta
import re

BRAIN_FILE = "second_brain.json"


def _load_brain_data():
    """Load the second brain knowledge base."""
    try:
        with open(BRAIN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        default = {
            "notes": [],
            "knowledge_base": {},
            "daily_insights": [],
            "habits": [],
            "projects": [],
            "learning_log": [],
            "quick_facts": {},
            "question_log": [],
            "tags": {},
            "connections": [],  # Relationships between concepts
            "statistics": {
                "total_notes": 0,
                "topics_tracked": 0,
                "habits_active": 0,
                "insights_generated": 0,
            }
        }
        _save_brain_data(default)
        return default


def _save_brain_data(data):
    """Save the second brain knowledge base."""
    with open(BRAIN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ================= NOTE-TAKING =================

def add_note(content, topic="general", tags=None):
    """Add a note to the second brain."""
    if not content or not content.strip():
        return "Note is empty. Please add some content."
    
    data = _load_brain_data()
    
    # Auto-detect tags from content if not provided
    if not tags:
        tags = _extract_tags(content)
    
    note = {
        "id": len(data["notes"]) + 1,
        "content": content.strip(),
        "topic": topic.lower(),
        "tags": tags,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "importance": "normal",  # Can be "high", "normal", "low"
        "linked_to": [],  # IDs of related notes
    }
    
    data["notes"].append(note)
    
    # Update statistics
    data["statistics"]["total_notes"] = len(data["notes"])
    
    # Track topic
    if topic not in data["knowledge_base"]:
        data["knowledge_base"][topic] = {"notes": [], "key_points": []}
        data["statistics"]["topics_tracked"] += 1
    
    data["knowledge_base"][topic]["notes"].append(note["id"])
    
    # Index tags
    for tag in tags:
        if tag not in data["tags"]:
            data["tags"][tag] = []
        data["tags"][tag].append(note["id"])
    
    _save_brain_data(data)
    return f"Note #{note['id']} saved in '{topic}' topic with tags: {', '.join(tags) if tags else 'none'}"


def _extract_tags(content):
    """Extract potential tags from content."""
    # Look for #hashtags
    hashtags = re.findall(r'#(\w+)', content)
    if hashtags:
        return [tag.lower() for tag in hashtags]
    
    # Look for capitalized words that might be entities
    words = content.split()
    potential_tags = [w.lower() for w in words if w[0].isupper() and len(w) > 3]
    return potential_tags[:3]  # Limit to 3 tags


def search_notes(query):
    """Search notes by keyword, tag, or topic."""
    data = _load_brain_data()
    query_lower = query.lower()
    
    results = []
    
    # Search in content
    for note in data["notes"]:
        if query_lower in note["content"].lower():
            results.append(note)
        elif query_lower in note.get("topic", "").lower():
            results.append(note)
        elif any(query_lower in tag.lower() for tag in note.get("tags", [])):
            results.append(note)
    
    if not results:
        return f"No notes found for '{query}'"
    
    # Sort by recency
    results.sort(key=lambda x: x["created"], reverse=True)
    
    output = f"Found {len(results)} note(s) for '{query}':\n\n"
    for r in results[:5]:  # Show top 5
        output += f"  [#{r['id']}] {r['created']} ({r['topic']})\n"
        output += f"  {r['content'][:100]}...\n"
        if r.get("tags"):
            output += f"  Tags: {', '.join(r['tags'])}\n"
        output += "\n"
    
    return output


def get_notes_by_topic(topic):
    """Get all notes for a specific topic."""
    data = _load_brain_data()
    topic_lower = topic.lower()
    
    if topic_lower not in data["knowledge_base"]:
        return f"No notes found for topic '{topic}'"
    
    note_ids = data["knowledge_base"][topic_lower]["notes"]
    notes = [n for n in data["notes"] if n["id"] in note_ids]
    
    if not notes:
        return f"No notes in '{topic}' topic"
    
    output = f"Notes in '{topic}' topic ({len(notes)} total):\n\n"
    for note in notes[-10:]:  # Show last 10
        output += f"  [#{note['id']}] {note['created']}\n"
        output += f"  {note['content'][:80]}...\n\n"
    
    return output


# ================= DAILY INSIGHTS =================

def add_insight(insight, category="general"):
    """Record a daily insight or learning."""
    data = _load_brain_data()
    
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "insight": insight,
        "category": category.lower(),
    }
    
    data["daily_insights"].append(entry)
    data["statistics"]["insights_generated"] += 1
    _save_brain_data(data)
    
    return f"Insight recorded: {insight[:50]}..."


def get_today_insights():
    """Show today's insights."""
    data = _load_brain_data()
    today = datetime.now().strftime("%Y-%m-%d")
    
    today_insights = [i for i in data["daily_insights"] if i["date"] == today]
    
    if not today_insights:
        return "No insights recorded for today yet."
    
    output = f"Today's Insights ({len(today_insights)} total):\n\n"
    for insight in today_insights:
        output += f"  [{insight['time']}] {insight['category'].upper()}\n"
        output += f"  {insight['insight']}\n\n"
    
    return output


def get_week_summary():
    """Generate weekly summary of insights and learnings."""
    data = _load_brain_data()
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")
    
    week_insights = [i for i in data["daily_insights"] 
                     if week_ago <= i["date"] <= today]
    
    if not week_insights:
        return "No insights recorded in the past week."
    
    # Group by category
    by_category = {}
    for insight in week_insights:
        cat = insight["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(insight["insight"])
    
    output = f"Weekly Summary (past 7 days, {len(week_insights)} insights):\n\n"
    for category, insights in by_category.items():
        output += f"  {category.upper()} ({len(insights)} insights)\n"
        for insight in insights[:3]:  # Show top 3 per category
            output += f"    - {insight[:70]}\n"
        output += "\n"
    
    return output


# ================= HABIT TRACKING =================

def add_habit(habit_name, frequency="daily"):
    """Start tracking a new habit."""
    data = _load_brain_data()
    
    habit = {
        "id": len(data["habits"]) + 1,
        "name": habit_name,
        "frequency": frequency,  # daily, weekly, monthly
        "started": datetime.now().strftime("%Y-%m-%d"),
        "streak": 0,
        "completions": [],
    }
    
    data["habits"].append(habit)
    data["statistics"]["habits_active"] = len([h for h in data["habits"]])
    _save_brain_data(data)
    
    return f"Tracking habit: '{habit_name}' ({frequency})"


def log_habit_completion(habit_id):
    """Log that a habit was completed today."""
    data = _load_brain_data()
    today = datetime.now().strftime("%Y-%m-%d")
    
    for habit in data["habits"]:
        if habit["id"] == habit_id:
            # Check if already logged today
            if today in habit["completions"]:
                return f"Already logged '{habit['name']}' for today."
            
            habit["completions"].append(today)
            habit["streak"] += 1
            _save_brain_data(data)
            return f"Logged '{habit['name']}' - {habit['streak']} day streak!"
    
    return f"Habit #{habit_id} not found."


def get_habit_status():
    """Show current habit tracking status."""
    data = _load_brain_data()
    
    if not data["habits"]:
        return "No habits being tracked yet. Try 'add habit' to start!"
    
    today = datetime.now().strftime("%Y-%m-%d")
    output = f"Habit Tracker ({len(data['habits'])} habits):\n\n"
    
    for habit in data["habits"]:
        completed_today = today in habit["completions"]
        status = "✓" if completed_today else " "
        output += f"  [{status}] {habit['name']}\n"
        output += f"      Streak: {habit['streak']} days | Frequency: {habit['frequency']}\n"
    
    return output


# ================= PROJECT TRACKING =================

def add_project(project_name, description="", tags=None):
    """Track a project."""
    data = _load_brain_data()
    
    project = {
        "id": len(data["projects"]) + 1,
        "name": project_name,
        "description": description,
        "tags": tags or [],
        "started": datetime.now().strftime("%Y-%m-%d"),
        "status": "active",  # active, paused, completed
        "progress": 0,
        "milestones": [],
    }
    
    data["projects"].append(project)
    _save_brain_data(data)
    
    return f"Project added: '{project_name}' (ID: {project['id']})"


def update_project_progress(project_id, progress):
    """Update project progress (0-100)."""
    data = _load_brain_data()
    
    for project in data["projects"]:
        if project["id"] == project_id:
            project["progress"] = min(100, max(0, progress))
            if progress == 100:
                project["status"] = "completed"
            _save_brain_data(data)
            return f"'{project['name']}' progress: {project['progress']}%"
    
    return f"Project #{project_id} not found."


def get_projects_status():
    """Show all active projects."""
    data = _load_brain_data()
    active = [p for p in data["projects"] if p["status"] != "completed"]
    
    if not active:
        return "No active projects. Start a new one with 'add project'!"
    
    output = f"Active Projects ({len(active)}):\n\n"
    for proj in active:
        bar_length = 20
        filled = int(bar_length * proj["progress"] / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        output += f"  [{bar}] {proj['progress']}%\n"
        output += f"  {proj['name']}\n"
        if proj["description"]:
            output += f"  {proj['description'][:60]}\n"
        output += "\n"
    
    return output


# ================= LEARNING LOG =================

def add_learning(topic, what_learned, source=""):
    """Log something new learned."""
    data = _load_brain_data()
    
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "topic": topic,
        "learning": what_learned,
        "source": source,
    }
    
    data["learning_log"].append(entry)
    _save_brain_data(data)
    
    return f"Learning logged: {topic} - {what_learned[:40]}..."


def get_learning_log(topic=None):
    """Show learning log, optionally filtered by topic."""
    data = _load_brain_data()
    
    entries = data["learning_log"]
    if topic:
        entries = [e for e in entries if topic.lower() in e["topic"].lower()]
    
    if not entries:
        return "Learning log is empty!"
    
    output = f"Learning Log ({len(entries)} entries"
    if topic:
        output += f" for '{topic}'"
    output += "):\n\n"
    
    for entry in entries[-10:]:  # Show last 10
        output += f"  [{entry['date']}] {entry['topic']}\n"
        output += f"  {entry['learning']}\n"
        if entry.get("source"):
            output += f"  Source: {entry['source']}\n"
        output += "\n"
    
    return output


# ================= BRAIN STATUS & STATS =================

def get_brain_status():
    """Show comprehensive brain statistics."""
    data = _load_brain_data()
    stats = data["statistics"]
    
    output = "Second Brain Status:\n\n"
    output += f"  Total Notes: {stats['total_notes']}\n"
    output += f"  Topics Tracked: {stats['topics_tracked']}\n"
    output += f"  Active Habits: {stats['habits_active']}\n"
    output += f"  Insights Generated: {stats['insights_generated']}\n"
    output += f"  Projects: {len(data['projects'])}\n"
    output += f"  Learning Entries: {len(data['learning_log'])}\n\n"
    
    # Top tags
    if data["tags"]:
        top_tags = sorted(data["tags"].items(), key=lambda x: len(x[1]), reverse=True)[:5]
        output += "  Top Tags:\n"
        for tag, notes in top_tags:
            output += f"    #{tag}: {len(notes)} notes\n"
    
    return output


def detect_brain_intent(text):
    """Detect if user wants to use second brain features."""
    t = text.lower()
    
    # Note-taking
    if any(p in t for p in ["note:", "remember:", "jot down", "add note", "take note", "note that"]):
        return ("add_note", {"content": text})
    
    if any(p in t for p in ["search notes", "find notes", "search for"]):
        query = text.replace("search notes", "").replace("find notes", "").replace("search for", "").strip()
        return ("search_notes", {"query": query})
    
    if any(p in t for p in ["my notes", "notes on", "get notes"]):
        topic = text.replace("my notes", "").replace("notes on", "").replace("get notes", "").strip()
        return ("get_notes_by_topic", {"topic": topic or "general"})
    
    # Insights
    if any(p in t for p in ["today insights", "today's insights", "my insights"]):
        return ("get_today_insights", {})
    
    if any(p in t for p in ["week summary", "weekly summary", "this week"]):
        return ("get_week_summary", {})
    
    if any(p in t for p in ["insight:", "learned that", "realized that"]):
        return ("add_insight", {"insight": text})
    
    # Habits
    if any(p in t for p in ["add habit", "track habit", "start tracking"]):
        return ("add_habit", {"habit_name": text})
    
    if any(p in t for p in ["habit status", "my habits", "habits tracked"]):
        return ("get_habit_status", {})
    
    if any(p in t for p in ["completed", "done with"]):
        # Assume it's a habit completion (will need more context)
        return ("log_habit_completion", {"habit_id": 1})
    
    # Projects
    if any(p in t for p in ["add project", "start project", "new project"]):
        return ("add_project", {"project_name": text})
    
    if any(p in t for p in ["project status", "my projects", "active projects"]):
        return ("get_projects_status", {})
    
    if any(p in t for p in ["progress", "update progress"]):
        return ("update_project_progress", {"project_id": 1, "progress": 50})
    
    # Learning
    if any(p in t for p in ["learned:", "learning:", "learned that", "add learning"]):
        return ("add_learning", {"topic": "general", "what_learned": text})
    
    if any(p in t for p in ["learning log", "what i learned"]):
        return ("get_learning_log", {})
    
    # Brain status
    if any(p in t for p in ["brain status", "second brain", "brain stats"]):
        return ("get_brain_status", {})
    
    return None


def execute_brain_action(action, args):
    """Execute a second brain action."""
    actions = {
        "add_note": add_note,
        "search_notes": search_notes,
        "get_notes_by_topic": get_notes_by_topic,
        "add_insight": add_insight,
        "get_today_insights": get_today_insights,
        "get_week_summary": get_week_summary,
        "add_habit": add_habit,
        "log_habit_completion": log_habit_completion,
        "get_habit_status": get_habit_status,
        "add_project": add_project,
        "update_project_progress": update_project_progress,
        "get_projects_status": get_projects_status,
        "add_learning": add_learning,
        "get_learning_log": get_learning_log,
        "get_brain_status": get_brain_status,
    }
    
    fn = actions.get(action)
    if fn:
        try:
            return fn(**args)
        except TypeError:
            # Try without kwargs if they don't match
            if action == "add_note":
                content = args.get("content", "")
                return add_note(content, args.get("topic", "general"), args.get("tags"))
            elif action == "add_insight":
                return add_insight(args.get("insight", ""), args.get("category", "general"))
            elif action == "add_habit":
                return add_habit(args.get("habit_name", ""), args.get("frequency", "daily"))
        return None
    
    return None
