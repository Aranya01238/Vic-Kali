"""Minimal test for 3 questions to diagnose hanging."""

from brain import think
import time

questions = [
    ("science", "What is quantum entanglement?"),
    ("social", "How are you?"),
    ("system", "Calculate 10 + 5"),
]

for idx, (cat, prompt) in enumerate(questions, 1):
    print(f"\nTest {idx}: [{cat}] {prompt}", flush=True)
    start = time.time()
    
    try:
        result = think(prompt)
        elapsed = time.time() - start
        
        result_short = str(result)[:80].replace('\n', ' ')
        print(f"✓ Response ({elapsed:.2f}s): {result_short}", flush=True)
    except Exception as e:
        elapsed = time.time() - start
        print(f"✗ Error ({elapsed:.2f}s): {str(e)[:60]}", flush=True)

print("\nDone!", flush=True)
