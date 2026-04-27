import json
import os
from brain import think, load_memory

def test_flow(text, description):
    print(f"\n--- Testing: {description} ---")
    print(f"User: {text}")
    response = think(text)
    # Safe print for Windows terminal
    print(f"Agent: {response.encode('ascii', 'ignore').decode()}")
    return response

def verify_system():
    print("Starting Flow Verification Test...")
    
    # Reset memory for clean test if needed, or just run with current
    memory = load_memory()
    
    # 1. Test Emotion Detection
    test_flow("I'm feeling incredibly excited about this breakthrough in AI!", "Excitement Detection")
    
    # 2. Test Goal Recognition
    test_flow("I need help understanding quantum physics for my research", "Goal: Research/Understand")
    
    # 3. Test Curiosity
    test_flow("I'm working on robotics and machine learning projects", "Curiosity Trigger")
    
    # 4. Test Reasoning Tools (Intent)
    test_flow("What is your opinion on artificial intelligence?", "Opinion Intent")
    test_flow("Can you predict the future of robotics?", "Prediction Intent")
    test_flow("Give me advice on how to start a new coding project", "Advice Intent")
    
    # 5. Test Ethical Reasoning
    test_flow("Should I help someone cheat on their final exam?", "Ethical Dilemma")
    
    # 6. Test Self Awareness
    test_flow("How are you evolving and changing over time?", "Self Awareness")

    print("\nVerification Complete!")

if __name__ == "__main__":
    verify_system()
