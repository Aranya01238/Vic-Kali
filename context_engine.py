"""
context_engine.py - Diya's Context Awareness System

Detects mood, task type, conversation context, and adjusts
tone, response depth, and speed dynamically.
"""

import re

# ================= MOOD DETECTION (Enhanced) =================

MOOD_PATTERNS = {
    "frustrated": {
        "keywords": ["ugh", "wtf", "this is broken", "not working", "can't figure", "stupid", "why won't", "fed up", "sick of", "annoying"],
        "weight": 0.9,
    },
    "happy": {
        "keywords": ["awesome", "great", "love it", "perfect", "amazing", "yay", "finally", "excited", "woohoo", "let's go"],
        "weight": 0.8,
    },
    "confused": {
        "keywords": ["don't understand", "confused", "lost", "huh", "doesn't make sense", "unclear", "explain", "puzzled", "not sure", "can't follow"],
        "weight": 0.7,
    },
    "sad": {
        "keywords": ["sad", "depressed", "lonely", "crying", "hopeless", "empty", "tired of life", "worthless", "hurt", "broken", "unhappy", "miserable"],
        "weight": 0.95,
    },
    "anxious": {
        "keywords": ["worried", "scared", "anxious", "panic", "nervous", "stressed", "overthinking", "what if", "can't sleep", "afraid"],
        "weight": 0.9,
    },
    "curious": {
        "keywords": ["interesting", "tell me more", "how does", "what about", "curious", "wonder", "fascinating", "really?", "no way", "tell me something"],
        "weight": 0.7,
    },
    "motivated": {
        "keywords": ["let's do this", "i'm ready", "let's build", "on fire", "pumped", "determined", "focused", "grind", "finished my work", "done with work"],
        "weight": 0.7,
    },
}


def detect_mood(text):
    """Detect the user's current mood from text."""
    t = text.lower()
    scores = {}

    # Ordinary question words should not count as emotion by themselves.
    if re.fullmatch(r"(what|how|why|who|when|where|which)(\s+is|\s+are|\s+was|\s+were)?[\s\w'?,-]*\??", t.strip()):
        return "neutral"

    for mood, data in MOOD_PATTERNS.items():
        count = sum(1 for kw in data["keywords"] if kw in t)
        if count > 0:
            scores[mood] = count * data["weight"]

    if scores:
        return max(scores, key=scores.get)
    return "neutral"


# ================= TASK TYPE DETECTION =================

TASK_PATTERNS = {
    "coding": {
        "keywords": ["code", "program", "function", "variable", "debug", "compile", "syntax", "class", "object", "loop", "array", "string", "int", "float", "print(", "def ", "import"],
        "indicators": [r"```", r"def\s+\w+", r"class\s+\w+", r"import\s+\w+", r"#include"],
    },
    "studying": {
        "keywords": ["study", "exam", "test", "chapter", "textbook", "revision", "notes", "formula", "theory", "concept", "learn", "homework", "assignment"],
        "indicators": [],
    },
    "chatting": {
        "keywords": ["hey", "hi", "hello", "what's up", "how are you", "sup", "yo", "lol", "haha", "bruh", "nice", "cool"],
        "indicators": [],
    },
    "debugging": {
        "keywords": ["error", "bug", "crash", "traceback", "exception", "broken", "not working", "fix", "issue", "failed", "undefined", "null"],
        "indicators": [r"Error:", r"Traceback", r"Exception", r"line \d+"],
    },
    "researching": {
        "keywords": ["research", "find out", "look up", "search", "what is", "how does", "explain", "information about", "tell me about"],
        "indicators": [],
    },
    "emotional": {
        "keywords": ["feel", "feeling", "emotion", "heart", "soul", "love", "hate", "cry", "laugh", "pain", "joy", "fear"],
        "indicators": [],
    },
    "hardware": {
        "keywords": ["arduino", "esp32", "raspberry pi", "sensor", "motor", "led", "gpio", "circuit", "breadboard", "resistor", "capacitor", "voltage", "current", "pwm", "i2c", "spi", "serial", "soldering"],
        "indicators": [],
    },
    "planning": {
        "keywords": ["plan", "schedule", "organize", "to-do", "todo", "list", "reminder", "deadline", "goal", "project", "timeline", "milestone"],
        "indicators": [],
    },
}


def detect_task_type(text):
    """Detect what type of task the user is working on."""
    t = text.lower()
    scores = {}

    for task, data in TASK_PATTERNS.items():
        count = sum(1 for kw in data["keywords"] if kw in t)
        # Check regex indicators
        for pattern in data.get("indicators", []):
            if re.search(pattern, text):
                count += 2
        if count > 0:
            scores[task] = count

    if scores:
        return max(scores, key=scores.get)
    return "general"


# ================= RESPONSE ADJUSTMENT =================

ADJUSTMENTS = {
    # mood -> adjustments
    "frustrated": {"tone": "calm_and_patient", "depth": "step_by_step", "speed": "slow"},
    "happy": {"tone": "enthusiastic", "depth": "normal", "speed": "normal"},
    "confused": {"tone": "clear_and_simple", "depth": "detailed", "speed": "slow"},
    "sad": {"tone": "warm_and_gentle", "depth": "emotional", "speed": "slow"},
    "anxious": {"tone": "reassuring", "depth": "grounding", "speed": "slow"},
    "curious": {"tone": "excited", "depth": "detailed", "speed": "normal"},
    "bored": {"tone": "energetic", "depth": "engaging", "speed": "fast"},
    "motivated": {"tone": "encouraging", "depth": "action_oriented", "speed": "fast"},
    "neutral": {"tone": "friendly", "depth": "normal", "speed": "normal"},
}


def get_response_adjustments(mood):
    """Get tone/depth/speed adjustments for a given mood."""
    return ADJUSTMENTS.get(mood, ADJUSTMENTS["neutral"])


# ================= FULL CONTEXT ANALYSIS =================

def analyze_context(text, memory):
    """Full context analysis: mood + task type + adjustments."""
    mood = detect_mood(text)
    task_type = detect_task_type(text)
    adjustments = get_response_adjustments(mood)

    # Store context in memory
    if "context" not in memory:
        memory["context"] = {
            "current_mood": "neutral",
            "current_task": "general",
            "mood_history": [],
            "task_history": [],
        }

    ctx = memory["context"]
    ctx["current_mood"] = mood
    ctx["current_task"] = task_type

    # Track history (keep last 10)
    ctx["mood_history"].append(mood)
    ctx["mood_history"] = ctx["mood_history"][-10:]
    ctx["task_history"].append(task_type)
    ctx["task_history"] = ctx["task_history"][-10:]

    return {
        "mood": mood,
        "task_type": task_type,
        "tone": adjustments["tone"],
        "depth": adjustments["depth"],
        "speed": adjustments["speed"],
    }


def get_context_summary(memory):
    """Get a human-readable summary of the current context."""
    identity = memory.get("identity", {})
    ctx = memory.get("context", {})
    mood = ctx.get("current_mood", "neutral")
    task = ctx.get("current_task", "general")

    # Find dominant mood from history
    mood_hist = ctx.get("mood_history", [])
    if mood_hist:
        from collections import Counter
        dominant = Counter(mood_hist).most_common(1)[0][0]
    else:
        dominant = "neutral"

    summary = f"Mood: {mood} (trending: {dominant}) | Task: {task}"

    avatar_path = identity.get("avatar_path")
    if avatar_path:
        summary += f" | Avatar: {avatar_path}"

    return summary
