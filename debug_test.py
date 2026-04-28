"""Quick debug test to verify basic test harness flow."""

from brain import think
import time

print("Test 1: Simple question", flush=True)
start = time.time()
result = think("How are you?")
elapsed = time.time() - start
print(f"Result: {result[:100]}", flush=True)
print(f"Time: {elapsed:.2f}s", flush=True)
print(flush=True)

print("Test 2: Science question", flush=True)
start = time.time()
result = think("What is quantum entanglement?")
elapsed = time.time() - start
print(f"Result: {result[:100]}", flush=True)
print(f"Time: {elapsed:.2f}s", flush=True)
print(flush=True)

print("All debug tests passed.", flush=True)
