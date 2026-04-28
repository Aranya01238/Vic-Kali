"""Trace web_search calls more carefully."""

import sys
import os
sys.path.insert(0, '.')
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Monkey-patch run_tool to trace calls
from tool_registry import run_tool as original_run_tool
calls = []

def traced_run_tool(tool_name, **kwargs):
    import traceback
    calls.append({
        'tool': tool_name,
        'args': kwargs,
        'trace': ''.join(traceback.format_stack()[-4:-1])
    })
    return original_run_tool(tool_name, **kwargs)

import tool_registry
tool_registry.run_tool = traced_run_tool

# Now import and test
from brain import think, detect_tool_intent, load_memory

memory = load_memory()

print("=" * 60, flush=True)
print("Testing: How are you?", flush=True)
print("=" * 60, flush=True)

# First check what detect_tool_intent returns
lower_text = "how are you?"
tool_name, args = detect_tool_intent(lower_text, memory)
print(f"\ndetect_tool_intent() returned: {tool_name}, {args}", flush=True)

# Now call think
result = think("How are you?")
result_clean = ''.join(c for c in str(result) if ord(c) < 256)[:100]
print(f"Result: {result_clean}", flush=True)

if calls:
    print(f"\nTool calls made: {len(calls)}", flush=True)
    for i, call in enumerate(calls, 1):
        print(f"\nCall #{i}: {call['tool']}", flush=True)
        print(f"Args: {call['args']}", flush=True)
else:
    print("\nNo tool calls made", flush=True)
