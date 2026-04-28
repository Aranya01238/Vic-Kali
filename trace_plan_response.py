"""Detailed trace of plan_response execution for 'how are you'."""

import sys
sys.path.insert(0, '.')

from brain import load_memory, get_current_state

memory = load_memory()
t = "how are you?"
state = get_current_state()

print(f"Input: {t}", flush=True)
print(f"State: {state}", flush=True)
print(flush=True)

# Check social_prompts pattern
social_prompts = [
    "how are you",
    "how are u",
    "how r u",
    "hows it going",
    "how's it going",
    "what's up",
    "whats up",
    "sup",
    "hello",
    "hi",
    "hey",
]

result = any(phrase in t for phrase in social_prompts)
print(f"Social prompts check: {result}", flush=True)

# Check which phrase matched
for phrase in social_prompts:
    if phrase in t:
        print(f"  Matched: '{phrase}'", flush=True)

# Check question pattern
result_q = "?" in t or any(t.startswith(w) for w in ["what", "how", "why", "who", "when", "where", "tell me", "explain"])
print(f"Question pattern check: {result_q}", flush=True)

# If both match, which one executes first?
print(flush=True)
print("Execution order in plan_response():", flush=True)
print("1. Social check comes BEFORE question fallback", flush=True)
print("2. So social should execute and return early", flush=True)
