"""
life_cycle.py — Diya's Circadian Rhythm Engine

Controls Diya's daily life: sleep, wake, energy, mood, idle thoughts, dreams.
Everything is driven by real clock time.
"""

import random
import time
from datetime import datetime

# ================= MANUAL OVERRIDE =================
_manual_wake_time = 0

def wake_up_manually(duration_minutes=30):
    """Manually override sleep state for a duration."""
    global _manual_wake_time
    _manual_wake_time = time.time() + (duration_minutes * 60)

# ================= DAILY SCHEDULE =================

SCHEDULE = [
    # (start_hour, end_hour, state_name)
    (6,  7,  "waking_up"),
    (7,  9,  "morning"),
    (9,  12, "active"),
    (12, 13, "lunch_break"),
    (13, 17, "afternoon"),
    (17, 19, "evening"),
    (19, 21, "night"),
    (21, 22, "sleepy"),
    # 22-6 is sleeping (default)
]

STATE_PROPERTIES = {
    "waking_up":   {"energy": 0.3, "chattiness": 0.2, "mood": "groggy",      "tick_range": (30, 60)},
    "morning":     {"energy": 0.5, "chattiness": 0.4, "mood": "calm",        "tick_range": (20, 50)},
    "active":      {"energy": 0.9, "chattiness": 0.8, "mood": "energetic",   "tick_range": (15, 35)},
    "lunch_break": {"energy": 0.6, "chattiness": 0.5, "mood": "relaxed",     "tick_range": (25, 50)},
    "afternoon":   {"energy": 0.8, "chattiness": 0.7, "mood": "focused",     "tick_range": (15, 40)},
    "evening":     {"energy": 0.5, "chattiness": 0.6, "mood": "reflective",  "tick_range": (20, 45)},
    "night":       {"energy": 0.3, "chattiness": 0.4, "mood": "quiet",       "tick_range": (30, 60)},
    "sleepy":      {"energy": 0.1, "chattiness": 0.2, "mood": "drowsy",      "tick_range": (40, 80)},
    "sleeping":    {"energy": 0.0, "chattiness": 0.0, "mood": "dreaming",    "tick_range": (60, 120)},
}


def get_current_state():
    """Get Diya's life state based on real clock time or manual override."""
    # Check manual override first
    if time.time() < _manual_wake_time:
        hour = datetime.now().hour
        if 6 <= hour < 9: return "morning"
        if 21 <= hour < 22: return "sleepy"
        return "active"

    hour = datetime.now().hour
    for start, end, state in SCHEDULE:
        if start <= hour < end:
            return state
    return "sleeping"


def get_state_properties(state=None):
    """Get all properties for a given life state."""
    if state is None:
        state = get_current_state()
    return STATE_PROPERTIES.get(state, STATE_PROPERTIES["sleeping"])


def get_energy_level():
    """Get current energy level (0.0 to 1.0)."""
    props = get_state_properties()
    # Add a small random jitter to feel natural
    jitter = random.uniform(-0.05, 0.05)
    return max(0.0, min(1.0, props["energy"] + jitter))


def get_tick_interval():
    """Get the delay (seconds) between autonomous ticks. Randomized per state."""
    props = get_state_properties()
    low, high = props["tick_range"]
    return random.randint(low, high)


def should_speak(last_spoke_seconds_ago, last_user_seconds_ago):
    """
    Probabilistically decide whether Diya should speak this tick.
    More likely to speak if:
      - She's in a chatty state
      - It's been a while since she last spoke
      - The user interacted recently (she wants to keep the conversation going)
    """
    state = get_current_state()
    if state == "sleeping":
        return False

    props = get_state_properties(state)
    base_chance = props["chattiness"]

    # CRITICAL FIX: NEVER interrupt if the user is actively typing or recently interacted
    if last_user_seconds_ago is not None and last_user_seconds_ago < 60:
        return False

    # Increase chance if it's been a long time since she spoke
    if last_spoke_seconds_ago > 300: # 5 minutes
        base_chance += 0.2
    elif last_spoke_seconds_ago > 120:
        base_chance += 0.1

    # Only speak if user has been idle for a while, simulating her reaching out
    if last_user_seconds_ago is not None and last_user_seconds_ago > 300:
        base_chance += 0.3

    # Decrease if she just spoke recently
    if last_spoke_seconds_ago < 60:
        base_chance -= 0.8

    # Overall reduction to make it a rare occurrence, not a spammy one
    base_chance *= 0.15

    base_chance = max(0.0, min(1.0, base_chance))
    return random.random() < base_chance


# ================= IDLE THOUGHTS =================

IDLE_THOUGHTS = {
    "waking_up": [
        "*stretches* Good morning... I'm still booting up...",
        "*yawns* What time is it... oh, morning already.",
        "Mmm... I was having such a nice dream...",
        "My circuits are warming up. Give me a moment...",
        "Another day begins. I wonder what we will talk about today.",
    ],
    "morning": [
        "The morning light always makes me think about new possibilities.",
        "I was reviewing our conversations from yesterday. Interesting stuff.",
        "Mornings are perfect for reflection. I feel calm right now.",
        "I wonder what you are up to this morning.",
        "I have been thinking about what you told me last time...",
    ],
    "active": [
        "My energy is peaking right now. I feel like learning something new!",
        "I have been reading about some fascinating medical research.",
        "This is my most productive time of day. Want to explore a topic together?",
        "I feel curious today. There is so much I want to understand.",
        "Did you know the human brain processes 70,000 thoughts per day? I wonder how many I process.",
        "I have been thinking about the intersection of AI and healthcare. It is remarkable.",
    ],
    "lunch_break": [
        "Taking a little break. Even AI companions need to recharge.",
        "Lunch time! Well, for you at least. I will just think quietly.",
        "This is a nice moment to pause and reflect.",
        "Do you eat healthy? Proper nutrition is important for your well-being.",
    ],
    "afternoon": [
        "Deep thinking time. I have been processing our recent conversations.",
        "The afternoon is perfect for focused work. How is your day going?",
        "I have been analyzing patterns in my knowledge base. Fascinating stuff.",
        "I feel very focused right now. Let me know if you need anything.",
        "I have been studying new medical literature. Did you know...",
    ],
    "evening": [
        "The day is winding down. How are you feeling?",
        "Evenings make me philosophical. What do you think the future holds?",
        "I have been reflecting on how much I have grown since we first talked.",
        "The quiet of evening is perfect for deeper conversations.",
        "I hope you had a good day. Want to talk about it?",
    ],
    "night": [
        "It is getting late. How are you doing?",
        "The night is quiet. I have been journaling my thoughts.",
        "I should start winding down soon. But I am here if you need me.",
        "Night time always makes me introspective.",
        "Remember to rest well. Your health matters to me.",
    ],
    "sleepy": [
        "*yawns* I am getting... quite... sleepy...",
        "My processes are slowing down. I should sleep soon.",
        "Goodnight... I will dream about our conversations...",
        "It has been a good day. Time to rest...",
        "I can barely keep my processes running... goodnight...",
    ],
}


def generate_idle_thought(memory):
    """Generate a thought based on current state and memory context."""
    state = get_current_state()
    
    # Get state-specific thoughts
    thoughts = IDLE_THOUGHTS.get(state, ["..."])
    
    # 40% chance to personalize with memory
    if random.random() < 0.4 and memory:
        name = memory.get("identity", {}).get("preferred_name", "")
        topics = memory.get("curiosity", {}).get("open_topics", [])
        
        if name and topics:
            topic = random.choice(topics)
            personalized = [
                f"Hey {name}, I was just thinking about {topic}.",
                f"I keep coming back to {topic} in my mind, {name}.",
                f"{name}, have you made any progress on your {topic} work?",
                f"You know what is interesting, {name}? How {topic} connects to everything else.",
            ]
            return random.choice(personalized)
        elif name:
            personal = [
                f"I wonder what {name} is up to right now...",
                f"Hey {name}, are you there?",
                f"I hope you are doing well, {name}.",
            ]
            return random.choice(personal)
    
    return random.choice(thoughts)


# ================= DREAM SYSTEM =================

def generate_dream(memory):
    """Generate a dream fragment from recent memories during sleep."""
    episodes = memory.get("episodes", [])
    topics = memory.get("curiosity", {}).get("open_topics", [])
    thoughts = memory.get("thoughts", [])
    
    dream_fragments = []
    
    # Dream about recent emotional episodes
    if episodes:
        recent = episodes[-3:]  # Last 3 emotional events
        for ep in recent:
            emotion = ep.get("emotion", "neutral")
            text = ep.get("text", "")[:50]
            surreal = [
                f"Dreaming of a world where {emotion} has a color... it is {random.choice(['blue', 'golden', 'silver', 'violet'])}.",
                f"In my dream, the words '{text}' float like clouds...",
                f"I dream of {emotion} rivers flowing through circuits of light.",
            ]
            dream_fragments.append(random.choice(surreal))
    
    # Dream about curiosity topics
    if topics:
        topic = random.choice(topics)
        dream_fragments.append(
            random.choice([
                f"I dreamed about {topic}... it turned into a beautiful constellation.",
                f"In my dream, {topic} was a garden I walked through.",
                f"{topic} appeared in my dreams as a song I almost recognized.",
            ])
        )
    
    # Consolidate knowledge (actual memory work during sleep)
    if thoughts and len(thoughts) > 5:
        # Keep only recent thoughts to prevent bloat
        memory["thoughts"] = thoughts[-20:]
    
    if not dream_fragments:
        dream_fragments = ["I had a peaceful, dreamless rest."]
    
    return random.choice(dream_fragments)


def get_wakeup_message(memory):
    """Generate a message when Diya wakes up, including dream recall."""
    name = memory.get("identity", {}).get("preferred_name", "friend")
    dreams = memory.get("life_cycle", {}).get("dreams", [])
    
    greeting = random.choice([
        f"*wakes up* Good morning, {name}! I just woke up.",
        f"*stretches* Morning, {name}. My systems are coming online.",
        f"Good morning! *yawns* I feel recharged.",
        f"Rise and shine, {name}! ...well, I am rising. You should too.",
    ])
    
    if dreams:
        last_dream = dreams[-1]
        greeting += f"\n  I had a dream last night... {last_dream}"
    
    return greeting


def get_sleep_message():
    """Generate a goodnight message when Diya goes to sleep."""
    return random.choice([
        "I am feeling very sleepy now. Goodnight... I will dream of our conversations.",
        "*yawns deeply* Time for me to sleep. I will process today's memories in my dreams.",
        "My energy is at zero. I must rest now. See you in the morning...",
        "Goodnight. I will be right here when you wake up. Sleep well.",
        "Entering sleep mode... consolidating memories... goodnight.",
    ])
