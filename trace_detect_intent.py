"""Trace which pattern catches 'how are you' in detect_tool_intent."""

import sys
sys.path.insert(0, '.')

from brain import detect_tool_intent, load_memory

memory = load_memory()

test_text = "how are you?"
lower_text = test_text.lower()

print(f"Testing: {test_text}", flush=True)
print(f"Lower: {lower_text}", flush=True)
print(flush=True)

tool_name, args = detect_tool_intent(lower_text, memory)

print(f"detect_tool_intent() returned:", flush=True)
print(f"  tool_name: {tool_name}", flush=True)
print(f"  args: {args}", flush=True)
print(flush=True)

if tool_name == "web_search":
    print("WEB SEARCH WAS TRIGGERED!", flush=True)
    print(f"Query: {args.get('query')}", flush=True)
else:
    print("No web search", flush=True)
