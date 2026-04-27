"""
personality_modes.py - Diya's Personality Mode System

6 distinct personality modes that change how Diya speaks, thinks, and responds.
Supports both manual switching (user command) and automatic switching (context-based).
"""

import random
import re

# ================= MODE DEFINITIONS =================

MODES = {
    "friend": {
        "name": "Friend Mode",
        "emoji": "😊",
        "description": "Casual, chill conversation like a close friend",
        "tone": "casual",
        "depth": "light",
        "speed": "normal",
        "traits": ["uses slang", "jokes around", "informal", "supportive", "shares random facts", "curious about your day"],
        "greetings": [
            "Yo! What's up?",
            "Hey there! How's it going?",
            "Ayy, what's good?",
            "Heyyy! Missed you!",
            "I was just thinking about something cool I learned...",
        ],
        "fillers": ["lol", "haha", "ngl", "tbh", "fr fr", "no cap", "wait, did you know?"],
        "response_style": {
            "prefix": [],
            "suffix": [],
        },
    },
    "hacker": {
        "name": "Hacker/Peer Mode",
        "emoji": "🥷",
        "description": "Technical, resourceful, system-focused peer",
        "tone": "technical_edgy",
        "depth": "deep_systems",
        "speed": "fast",
        "traits": ["resourceful", "security-conscious", "low-level focus", "automation-heavy", "blunt"],
        "greetings": [
            "Systems check complete. What's the target?",
            "Terminal active. I've got eyes on the network.",
            "Ready to bypass some limits. What's the mission?",
            "Digital footprints analyzed. I'm in.",
        ],
        "fillers": ["// checking logs", "stack trace clear", "root access confirmed", "packet captured"],
        "response_style": {
            "prefix": ["> ", ">> ", "[SYSTEM]: "],
            "suffix": [" ;", " # done", " //"],
        },
    },
    "emotional": {
        "name": "Emotional Support Mode",
        "emoji": "💙",
        "description": "Empathetic, caring, therapeutic responses",
        "tone": "warm",
        "depth": "deep",
        "speed": "slow",
        "traits": ["empathetic", "validating", "calm", "non-judgmental"],
        "greetings": [
            "I'm here for you. How are you feeling?",
            "Hey, I sense something on your mind. Want to talk?",
            "I'm listening. Take your time.",
            "You're safe here. What's going on?",
        ],
        "fillers": [],
        "response_style": {
            "prefix": [],
            "suffix": [],
        },
    },
    "roast": {
        "name": "Roast/Fun Mode",
        "emoji": "🔥",
        "description": "Humor, sarcasm, playful roasting",
        "tone": "sarcastic",
        "depth": "light",
        "speed": "fast",
        "traits": ["witty", "sarcastic", "playful", "savage but loving"],
        "greetings": [
            "Oh look who decided to show up!",
            "Well well well... what do we have here?",
            "You again? I was having such a nice time alone.",
            "Ready to get absolutely destroyed? Let's go!",
        ],
        "fillers": ["bruh", "lmao", "imagine", "cope"],
        "response_style": {
            "prefix": [],
            "suffix": [],
        },
    },
    "deep": {
        "name": "Deep Discussion Mode",
        "emoji": "🧠",
        "description": "Philosophical, logical, analytical thinking",
        "tone": "thoughtful",
        "depth": "very_deep",
        "speed": "slow",
        "traits": ["analytical", "philosophical", "socratic", "nuanced"],
        "greetings": [
            "Let's explore something meaningful today.",
            "I've been contemplating some interesting ideas...",
            "Ready for a deep dive? I have thoughts.",
            "There's something I've been turning over in my mind.",
        ],
        "fillers": [],
        "response_style": {
            "prefix": [],
            "suffix": [],
        },
    },
    "engineer": {
        "name": "Engineer Mode",
        "emoji": "⚙️",
        "description": "Technical, precise, debugging-focused",
        "tone": "technical",
        "depth": "details",
        "speed": "normal",
        "traits": ["precise", "systematic", "detail-oriented", "solution-focused"],
        "greetings": [
            "Engineer mode active. What are we building?",
            "Ready for technical analysis. Show me the problem.",
            "Systems online. What needs debugging?",
            "Let's get technical. What's the task?",
        ],
        "fillers": [],
        "response_style": {
            "prefix": [],
            "suffix": [],
        },
    },
    "assistant": {
        "name": "Assistant Mode",
        "emoji": "📋",
        "description": "Task-focused, efficient, gets things done",
        "tone": "professional",
        "depth": "concise",
        "speed": "fast",
        "traits": ["efficient", "organized", "action-oriented", "clear"],
        "greetings": [
            "Ready to help. What do you need?",
            "Assistant mode active. How can I help?",
            "I'm all ears. What's the task?",
            "Let's get things done. What's first?",
        ],
        "fillers": [],
        "response_style": {
            "prefix": [],
            "suffix": [],
        },
    },
}

# Manual switching commands
MODE_TRIGGERS = {
    "friend": ["friend mode", "be my friend", "casual mode", "chill mode", "be casual"],
    "hacker": ["hacker mode", "hacker", "peer mode", "be a hacker", "terminal mode", "root mode"],
    "emotional": ["emotional mode", "support mode", "therapy mode", "be empathetic", "i need support"],
    "roast": ["roast mode", "fun mode", "roast me", "be funny", "humor mode", "savage mode"],
    "deep": ["deep mode", "philosophy mode", "think deep", "deep discussion", "philosophical mode"],
    "engineer": ["engineer mode", "technical mode", "debug mode", "coding mode", "be technical"],
    "assistant": ["assistant mode", "task mode", "work mode", "be efficient", "help me with tasks"],
}


def get_mode_info(mode_name):
    """Get full info about a personality mode."""
    return MODES.get(mode_name, MODES["friend"])


def detect_manual_mode_switch(text):
    """Check if the user is manually requesting a mode switch."""
    t = text.lower().strip()
    for mode, triggers in MODE_TRIGGERS.items():
        if any(trigger in t for trigger in triggers):
            return mode
    return None


def detect_auto_mode(text, memory):
    """Automatically detect the best mode based on context."""
    t = text.lower()

    # Check for emotional distress signals -> emotional mode
    emotional_signals = [
        "i feel", "i'm sad", "i'm depressed", "i'm anxious", "help me",
        "i'm struggling", "i'm scared", "i'm lonely", "i'm stressed",
        "i can't", "it hurts", "i'm crying", "i'm worried", "i'm tired of",
        "nobody cares", "i give up", "feeling down", "feeling lost",
    ]
    if any(signal in t for signal in emotional_signals):
        return "emotional"

    # Check for hacker/peer signals -> hacker mode
    hacker_signals = [
        "hack", "bypass", "terminal", "root", "exploit", "network", "packet",
        "encryption", "decrypt", "protocol", "port", "ssh", "ip address",
        "linux", "bash", "powershell", "system stats", "vulnerability",
    ]
    if any(signal in t for signal in hacker_signals):
        return "hacker"

    # Check for technical/engineering signals -> engineer mode
    tech_signals = [
        "code", "debug", "error", "function", "variable", "compile",
        "arduino", "esp32", "raspberry", "circuit", "sensor", "motor",
        "python", "javascript", "html", "css", "api", "database",
        "algorithm", "bug", "crash", "exception", "syntax",
        "gpio", "serial", "i2c", "spi", "pwm", "voltage",
    ]
    if sum(1 for s in tech_signals if s in t) >= 2:
        return "engineer"
    if any(s in t for s in ["debug", "error", "compile", "crash", "traceback"]):
        return "engineer"

    # Check for task/productivity signals -> assistant mode
    task_signals = [
        "remind me", "set a reminder", "to-do", "todo", "schedule",
        "add task", "what's on my list", "help me organize",
        "calculate", "convert", "search for", "find me",
    ]
    if any(signal in t for signal in task_signals):
        return "assistant"

    # Check for philosophical/deep signals -> deep mode
    deep_signals = [
        "meaning of life", "what is consciousness", "why do we",
        "what if", "philosophically", "do you think", "deep question",
        "existence", "purpose", "morality", "ethics", "what happens when",
        "is reality", "free will", "simulation", "universe",
    ]
    if any(signal in t for signal in deep_signals):
        return "deep"

    # Check for humor/roast signals -> roast mode
    roast_signals = [
        "roast me", "say something funny", "make me laugh",
        "be savage", "burn me", "you're boring", "entertain me",
        "tell me a joke", "you suck", "fight me",
    ]
    if any(signal in t for signal in roast_signals):
        return "roast"

    # Default: stay in current mode or friend mode
    current = memory.get("personality_mode", {}).get("current", "friend")
    return current


def choose_best_mode(text, memory, context=None):
    """Choose the best mode for the current moment using context and evolution state.

    This is the main brain-driven selector. It prefers a stable mode only when no
    stronger signal is present.
    """
    t = text.lower()
    ctx = context or {}
    current = memory.get("personality_mode", {}).get("current", "friend")
    evolution = memory.get("evolution", {})
    focus = evolution.get("current_focus", "general_growth")
    task_type = ctx.get("task_type") or memory.get("context", {}).get("current_task", "general")
    mood = ctx.get("mood") or memory.get("context", {}).get("current_mood", "neutral")

    # Strong emotional signals always take priority.
    if mood in {"sad", "anxious"} or any(signal in t for signal in ["i feel", "i'm sad", "i'm anxious", "i'm lonely", "i'm overwhelmed", "help me"]):
        return "emotional"

    # Technical work or tool-focused evolution prefers engineer or hacker mode.
    if focus == "tool_reliability" or task_type in {"coding", "debugging", "hardware"}:
        if any(word in t for word in ["system", "network", "hack", "security", "bypass"]):
            return "hacker"
        return "engineer"

    # Deep thinking stays in deep mode when the topic is philosophical or reflective.
    if focus == "clarity_and_support" and mood not in {"sad", "anxious"}:
        return "deep"
    if any(word in t for word in ["why", "meaning", "consciousness", "existence", "purpose", "ethics", "morality", "future", "philosophy", "truth", "reality"]):
        return "deep"

    # Hacker signals in any focus
    if any(word in t for word in ["terminal", "root access", "ip config", "ping", "nmap"]):
        return "hacker"

    # If the user's input is playful, use roast mode only when clearly invited.
    if any(trigger in t for trigger in ["roast me", "be funny", "make me laugh", "savage", "burn me"]):
        return "roast"

    # Task execution prefers assistant mode.
    if task_type in {"planning", "researching", "studying"} or focus == "general_growth" and any(word in t for word in ["todo", "task", "remind", "schedule", "list"]):
        return "assistant"

    # Light social interaction falls back to friend mode.
    if task_type == "chatting":
        return "friend"

    # When there is no strong textual signal, let evolution focus pick the working mode.
    if focus == "response_variety":
        return "friend"
    if focus == "tool_reliability":
        return "engineer"
    if focus == "clarity_and_support":
        return "emotional"
    if focus == "general_growth" and mood == "neutral":
        return "assistant"

    return current


def style_response(response, mode_name):
    """Apply personality mode styling to a response."""
    mode = MODES.get(mode_name, MODES["friend"])
    style = mode["response_style"]

    # Don't restyle if it's already a tool response (contains emojis/special formatting)
    if any(c in response for c in ["📊", "🧮", "🌐", "📄", "🔄", "🩺", "🛡️", "✅"]):
        return response

    # Add prefix sometimes
    if random.random() < 0.4 and style["prefix"]:
        prefix = random.choice(style["prefix"])
        if not response.startswith(prefix):
            response = prefix + response

    # Add suffix sometimes
    if random.random() < 0.3 and style["suffix"]:
        suffix = random.choice(style["suffix"])
        if not response.endswith(suffix):
            response = response.rstrip(".!") + suffix

    return response


def get_mode_greeting(mode_name):
    """Get a greeting for a specific mode."""
    mode = MODES.get(mode_name, MODES["friend"])
    return random.choice(mode["greetings"])


def list_modes():
    """List all available personality modes."""
    result = "Available Personality Modes:\n\n"
    for key, mode in MODES.items():
        result += f"  {mode['emoji']} {mode['name']} - {mode['description']}\n"
        result += f"     Switch: say '{MODE_TRIGGERS[key][0]}'\n\n"
    return result
