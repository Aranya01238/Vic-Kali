import random
from datetime import datetime

def scan_vitals():
    """Mock scanner for vital signs"""
    vitals = {
        "heart_rate": random.randint(60, 100),
        "temperature": round(random.uniform(36.5, 37.5), 1),
        "blood_pressure": f"{random.randint(110, 130)}/{random.randint(70, 90)}",
        "oxygen_level": random.randint(95, 100)
    }
    status = "Normal"
    if vitals["heart_rate"] > 100 or vitals["temperature"] > 38.0:
        status = "Elevated - Care recommended"
    
    return f"🩺 Scan complete. Vitals: HR: {vitals['heart_rate']} bpm, Temp: {vitals['temperature']}°C, BP: {vitals['blood_pressure']}, O2: {vitals['oxygen_level']}%.\nStatus: {status}"

def diagnose_issue(symptoms):
    """Instant diagnosis based on symptoms"""
    symptoms = symptoms.lower()
    database = {
        "headache": "Tension headache likely. Recommendation: Rest and hydration.",
        "fever": "Possible infection. Monitoring temperature. Stay hydrated.",
        "cough": "Respiratory irritation detected. Recommendation: Warm fluids.",
        "pain": "Localized discomfort. Please rate on a scale of 1 to 10.",
        "fracture": "Internal structural compromise detected. Immobilization required.",
        "cut": "Dermal laceration. First aid required: Clean and bandage.",
        "arm": "Discomfort in upper extremity detected. Please specify if it is sharp or dull pain.",
        "leg": "Lower extremity discomfort detected. Avoid putting weight on it.",
        "chest": "Chest discomfort detected. Monitoring heart rate. If pain persists, seek immediate medical attention.",
        "stomach": "Abdominal distress detected. Rest and avoid solid foods for now."
    }
    
    for symptom, diagnosis in database.items():
        if symptom in symptoms:
            return f"🏥 Diagnosis: {diagnosis}"
    
    return "🔬 Scanners are inconclusive. I require more data to provide an accurate diagnosis."

def first_aid_instruction(injury):
    """First aid instructions"""
    injury = injury.lower()
    instructions = {
        "burn": "1. Run cool water over the area for 10 minutes. 2. Cover loosely with sterile gauze.",
        "cut": "1. Apply pressure to stop bleeding. 2. Clean with mild soap and water. 3. Apply antibiotic ointment and bandage.",
        "sprain": "RICE protocol: Rest, Ice, Compression, Elevation.",
        "choking": "Perform Heimlich maneuver immediately. Call emergency services.",
        "allergic": "Administer antihistamine or epinephrine if available. Seek immediate medical help."
    }
    
    for key, text in instructions.items():
        if key in injury:
            return f"🩹 First Aid Instructions for {key.title()}:\n{text}"
    
    return "❓ Unknown injury. Please stay calm while I look up the best protocol."

def emotional_support_protocol(emotion):
    """Comforting patient based on emotion"""
    reassurances = {
        "sad": "I am sorry you are feeling sad. It is okay to cry. My inflatable body is designed for hugging.",
        "anxious": "Please focus on your breathing. I am here with you. You are safe.",
        "angry": "I detect elevated stress levels. Let us try a calming exercise.",
        "scared": "There is no immediate threat to your safety. I will remain by your side.",
        "happy": "Positive emotional state detected. This will aid in your overall well-being."
    }
    
    return reassurances.get(emotion.lower(), "I am here to support your emotional health.")

def combat_mode(enable=True):
    """Baymax's upgraded combat algorithms"""
    if enable:
        return "🛡️ Combat algorithms active. Armor deployed. Jet propulsion systems online. I will protect you."
    else:
        return "🏥 Combat mode deactivated. Returning to healthcare protocols."

def satisfaction_check(user_satisfied):
    """Deactivation protocol"""
    if user_satisfied:
        return "✅ Deactivating. I will remain in my charging station until you need me again. I am glad you are satisfied with your care."
    else:
        return "🤝 I cannot deactivate until you are satisfied with your care. How else can I assist you?"
