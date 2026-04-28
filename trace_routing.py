"""Debug tracing to find where social questions are being mislabeled."""

import sys
sys.path.insert(0, '.')

from brain import plan_response, load_memory

memory = load_memory()

# Test the plan_response function directly
test_prompts = [
    "How are you?",
    "How are u?",
    "What's up?",
    "Hi there",
    "What is quantum entanglement?",
]

print("Testing plan_response() directly:", flush=True)
print("=" * 60, flush=True)

for prompt in test_prompts:
    lower = prompt.lower()
    print(f"\nPrompt: {prompt}", flush=True)
    print(f"Lower: {lower}", flush=True)
    
    response = plan_response(memory, lower)
    print(f"Response (first 100 chars): {str(response)[:100]}", flush=True)
    
    if "🌐" in str(response):
        print("⚠️  WARNING: Web search detected!", flush=True)
    elif "I'm doing" in str(response) or "I'm good" in str(response):
        print("✓ Local social response", flush=True)
    else:
        print("? Unknown response type", flush=True)

print(flush=True)
print("=" * 60, flush=True)
