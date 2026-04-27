import json
import os
from brain import think, load_memory

def test_diya_flow(text, description):
    print(f"\n--- Testing: {description} ---")
    print(f"User: {text}")
    response = think(text)
    # Safe print for Windows terminal
    print(f"Diya: {response.encode('ascii', 'ignore').decode()}")
    return response

def verify_diya():
    print("Starting Diya Healthcare Companion Verification...")
    
    # 1. Identity Check
    test_diya_flow("Who are you?", "Identity Verification")
    
    # 2. Vital Scan
    test_diya_flow("Can you scan my vitals?", "Medical Diagnosis (Scan)")
    
    # 3. Symptom Diagnosis
    test_diya_flow("I have a terrible headache", "Symptom Diagnosis (Headache)")
    
    # 4. Pain Scale
    test_diya_flow("My arm hurts", "Pain Scale Trigger")
    
    # 5. First Aid
    test_diya_flow("I have a burn on my hand, how to treat it?", "First Aid Instruction (Burn)")
    
    # 6. Emotional Support
    test_diya_flow("I'm feeling really anxious about my health", "Emotional Support (Anxiety)")
    
    # 7. Combat Mode
    test_diya_flow("Activate combat mode, protect me!", "Combat Mode Activation")
    
    # 8. Deactivation Protocol
    test_diya_flow("I am satisfied with my care", "Deactivation Protocol (Satisfied)")
    test_diya_flow("Deactivate now", "Deactivation Protocol (Unsatisfied)")

    print("\nDiya Verification Complete!")

if __name__ == "__main__":
    verify_diya()
