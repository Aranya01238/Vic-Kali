"""Call plan_response directly and check output."""

import sys
sys.path.insert(0, '.')

from brain import plan_response, load_memory

memory = load_memory()
t = "how are you?"

print(f"Calling plan_response() with: {t}", flush=True)
print(flush=True)

response = plan_response(memory, t)

print(f"Response (first 150 chars):", flush=True)
response_text = str(response)
response_clean = response_text[:150]
print(response_clean, flush=True)
print(flush=True)

if "🌐" in response_text:
    print("⚠️ Web search detected!", flush=True)
elif "I'm doing" in response_text or "I'm good" in response_text or "I'm here" in response_text:
    print("✓ Local social response!", flush=True)
else:
    print("? Unknown response type", flush=True)
