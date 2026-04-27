"""Full system verification for Diya's upgraded capabilities."""
import json
import os
from brain import think, load_memory, save_memory

def test(text, label):
    print(f"\n{'='*55}")
    print(f"  TEST: {label}")
    print(f"{'='*55}")
    print(f"  You: {text}")
    response = think(text)
    safe = response.encode("ascii", "replace").decode()
    print(f"  Diya: {safe}")
    return response

def run_all_tests():
    print("DIYA FULL SYSTEM VERIFICATION")
    print("=" * 55)

    # 1. Personality Modes
    test("list modes", "List All Modes")
    test("roast mode", "Switch to Roast Mode")
    test("What do you think of me?", "Roast Response")
    test("engineer mode", "Switch to Engineer Mode")
    test("friend mode", "Switch Back to Friend Mode")

    # 2. Context Awareness
    test("I'm so frustrated this code won't compile!", "Mood: Frustrated")
    test("I'm feeling really sad today", "Mood: Sad (auto-switch to emotional)")
    test("status", "Show Context Status")

    # 3. Task Manager
    test("add task: finish the robotics project", "Add To-Do")
    test("add task: submit assignment", "Add Another To-Do")
    test("show tasks", "List To-Dos")
    test("remind me to take a break in 1 minutes", "Set Reminder")

    # 4. Engineering Assistant
    test("I have an error: NameError: name 'x' is not defined", "Error Analysis")
    test("Help me debug my ESP32, the sensor is not reading", "Hardware Debug")
    test("Recommend a project for a beginner in robotics", "Project Recommendation")

    # 5. Healthcare (Diya/Baymax)
    test("scan my vitals", "Health Scan")
    test("I have a headache", "Symptom Diagnosis")

    # 6. Identity
    test("who are you?", "Identity Check")

    # 7. Existing Tools
    test("what is the time", "Time Tool")
    test("calculate 25 * 4 + 10", "Calculator")

    print("\n" + "=" * 55)
    print("  ALL TESTS COMPLETE")
    print("=" * 55)

if __name__ == "__main__":
    run_all_tests()
