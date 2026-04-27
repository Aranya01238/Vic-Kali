"""
engineering_assistant.py - Diya's Engineering & Debug Assistant

Code analysis, hardware debugging guidance (ESP32, Arduino),
error detection, step-by-step troubleshooting, and project recommendations.
"""

import re

# ================= CODE ANALYSIS =================

def analyze_code(code):
    """Analyze code for common issues and provide suggestions."""
    issues = []
    suggestions = []
    language = detect_language(code)

    # Python-specific checks
    if language == "python":
        # Missing colons
        for i, line in enumerate(code.split("\n"), 1):
            stripped = line.strip()
            if stripped.startswith(("if ", "elif ", "else", "for ", "while ", "def ", "class ", "try", "except", "finally", "with ")):
                if stripped and not stripped.endswith(":") and not stripped.endswith(":\\"):
                    issues.append(f"Line {i}: Missing colon after '{stripped[:30]}...'")

            # Indentation issues
            if line and not line.startswith(" ") and not line.startswith("\t") and not stripped.startswith(("#", "import", "from", "def", "class", "if", "else", "elif", "for", "while", "try", "except", "finally", "with", "return", "print", "@")):
                if "=" in line and not line.strip().startswith("#"):
                    pass  # Variable assignment at top level is fine

        # Common mistakes
        if "print " in code and "print(" not in code:
            issues.append("Using Python 2 print syntax. Use print() instead.")
        if "raw_input" in code:
            issues.append("raw_input() is Python 2. Use input() in Python 3.")
        if "except:" in code:
            suggestions.append("Bare 'except:' catches all exceptions. Specify exception type.")
        if "import *" in code:
            suggestions.append("Wildcard imports (import *) can cause namespace pollution.")

    # C/C++/Arduino checks
    elif language in ("c", "cpp", "arduino"):
        for i, line in enumerate(code.split("\n"), 1):
            stripped = line.strip()
            # Missing semicolons
            if stripped and not stripped.endswith((";", "{", "}", "//", "*/", "*/")) and not stripped.startswith(("#", "//", "/*", "if", "else", "for", "while", "void", "int", "float", "char", "}")):
                if "=" in stripped or "(" in stripped:
                    issues.append(f"Line {i}: Possible missing semicolon")

        if "delay(" in code:
            suggestions.append("Consider using millis() instead of delay() for non-blocking code.")
        if "String " in code:
            suggestions.append("Arduino String class can cause memory fragmentation. Consider char arrays.")

    # JavaScript checks
    elif language == "javascript":
        if "var " in code:
            suggestions.append("Consider using 'let' or 'const' instead of 'var' (ES6+).")
        if "==" in code and "===" not in code:
            suggestions.append("Use === for strict equality comparison instead of ==.")
        if "document.write" in code:
            suggestions.append("Avoid document.write() - use DOM manipulation instead.")

    result = f"Code Analysis ({language.upper()}):\n\n"

    if issues:
        result += "Issues Found:\n"
        for issue in issues:
            result += f"  [!] {issue}\n"
    else:
        result += "No critical issues found.\n"

    if suggestions:
        result += "\nSuggestions:\n"
        for s in suggestions:
            result += f"  [*] {s}\n"

    result += f"\nLines of code: {len(code.split(chr(10)))}"
    return result


def detect_language(code):
    """Detect programming language from code content."""
    if "void setup()" in code or "void loop()" in code or "#include <Arduino" in code:
        return "arduino"
    if "#include" in code and ("int main" in code or "void " in code):
        return "cpp"
    if "def " in code or "import " in code or "print(" in code:
        return "python"
    if "function " in code or "const " in code or "document." in code or "=>" in code:
        return "javascript"
    if "<html" in code.lower() or "<div" in code.lower():
        return "html"
    if "{" in code and ":" in code and ";" in code:
        return "css"
    return "unknown"


# ================= HARDWARE DEBUGGING =================

HARDWARE_KB = {
    "esp32": {
        "common_issues": [
            "GPIO 6-11 are connected to SPI flash - avoid using them",
            "Use GPIO 34-39 for input only (no internal pull-up)",
            "Maximum GPIO current: 12mA per pin, 40mA total",
            "WiFi can cause brownout if power supply is weak (use 5V/1A+)",
            "Deep sleep current: ~10uA (use esp_deep_sleep_start())",
        ],
        "pin_guide": "Safe GPIOs: 2, 4, 5, 12-33. Input-only: 34-39. Avoid: 6-11.",
        "debug_tips": [
            "Check Serial Monitor at 115200 baud",
            "Use Serial.println() for debugging",
            "Check power supply voltage with multimeter",
            "Flash at 115200 baud rate if upload fails",
            "Hold BOOT button while uploading if needed",
        ],
    },
    "arduino": {
        "common_issues": [
            "Analog pins (A0-A5) can also be used as digital pins",
            "Maximum current per pin: 20mA (40mA absolute max)",
            "Total current from all pins: 200mA max",
            "Use external power for motors/servos (not USB power)",
            "Floating pins give random readings - use pull-up/pull-down",
        ],
        "pin_guide": "Digital: 0-13, Analog: A0-A5, PWM: 3,5,6,9,10,11",
        "debug_tips": [
            "Check Serial Monitor at 9600 baud (default)",
            "LED on pin 13 for quick debugging",
            "Use Serial.available() before Serial.read()",
            "Reset button if sketch freezes",
            "Check USB cable - some are charge-only",
        ],
    },
    "raspberry_pi": {
        "common_issues": [
            "GPIO voltage is 3.3V - NOT 5V tolerant",
            "Maximum current per GPIO: 16mA",
            "Use BCM or BOARD numbering consistently",
            "SD card corruption from sudden power loss",
            "WiFi can interfere with Bluetooth",
        ],
        "pin_guide": "GPIO 2-27 available. I2C: GPIO 2(SDA), 3(SCL). SPI: 7-11.",
        "debug_tips": [
            "Check with: gpio readall",
            "Use raspi-config for interface settings",
            "Monitor temperature: vcgencmd measure_temp",
            "Check logs: journalctl -xe",
            "Use SSH for headless debugging",
        ],
    },
}


def hardware_debug(board, issue=""):
    """Get hardware debugging guidance."""
    board = board.lower().replace(" ", "_").replace("-", "_")

    # Normalize board names
    if "esp" in board:
        board = "esp32"
    elif "arduino" in board or "uno" in board or "mega" in board or "nano" in board:
        board = "arduino"
    elif "raspberry" in board or "rpi" in board or "pi" in board:
        board = "raspberry_pi"

    hw = HARDWARE_KB.get(board)
    if not hw:
        return f"I don't have specific data for '{board}'. I support: ESP32, Arduino, Raspberry Pi."

    result = f"Hardware Debug Guide: {board.upper()}\n\n"
    result += f"Pin Guide: {hw['pin_guide']}\n\n"

    result += "Common Issues:\n"
    for issue_text in hw["common_issues"]:
        result += f"  [!] {issue_text}\n"

    result += "\nDebug Tips:\n"
    for tip in hw["debug_tips"]:
        result += f"  [*] {tip}\n"

    return result


# ================= ERROR DETECTION =================

def analyze_error(error_text):
    """Analyze an error message and provide troubleshooting steps."""
    t = error_text.lower()
    steps = []

    # Python errors
    if "syntaxerror" in t:
        steps = [
            "Check for missing colons (:) after if/for/def/class",
            "Check for unmatched parentheses/brackets",
            "Check for incorrect indentation",
            "Look at the line number in the error message",
            "Check for missing quotes in strings",
        ]
    elif "nameerror" in t:
        steps = [
            "Variable or function is not defined before use",
            "Check for typos in variable names",
            "Make sure imports are at the top of the file",
            "Check variable scope (local vs global)",
        ]
    elif "typeerror" in t:
        steps = [
            "You're using a wrong data type for an operation",
            "Check if you're mixing strings and numbers",
            "Verify function argument count and types",
            "Use type() to check variable types",
        ]
    elif "indexerror" in t:
        steps = [
            "List/array index is out of range",
            "Check list length with len() before accessing",
            "Remember: indices start at 0",
            "Use try/except to handle edge cases",
        ]
    elif "keyerror" in t:
        steps = [
            "Dictionary key does not exist",
            "Use .get(key, default) instead of dict[key]",
            "Check available keys with dict.keys()",
            "Verify JSON/data structure matches expectations",
        ]
    elif "importerror" in t or "modulenotfounderror" in t:
        steps = [
            "Module is not installed: pip install <module_name>",
            "Check if virtual environment is activated",
            "Verify Python version compatibility",
            "Check for circular imports",
        ]
    elif "attributeerror" in t:
        steps = [
            "Object doesn't have the attribute/method you're calling",
            "Check if variable is None (NoneType has no attributes)",
            "Verify the object type with type()",
            "Check documentation for correct method names",
        ]
    elif "filenotfounderror" in t:
        steps = [
            "File path is incorrect or file doesn't exist",
            "Use absolute paths or verify working directory",
            "Check file permissions",
            "Use os.path.exists() to verify before opening",
        ]
    # Arduino/C++ errors
    elif "was not declared" in t:
        steps = [
            "Variable or function used before declaration",
            "Check #include statements",
            "Declare variables before using them",
            "Check for typos in names",
        ]
    elif "expected" in t and "before" in t:
        steps = [
            "Missing semicolon, bracket, or parenthesis",
            "Check the line BEFORE the error line",
            "Verify matching braces {}",
            "Check function declarations",
        ]
    else:
        steps = [
            "Read the error message carefully - it usually tells you what's wrong",
            "Check the line number mentioned in the error",
            "Google the exact error message",
            "Try isolating the problem with print/debug statements",
            "Check recent changes that might have caused the issue",
        ]

    result = "Troubleshooting Steps:\n\n"
    for i, step in enumerate(steps, 1):
        result += f"  Step {i}: {step}\n"

    return result


# ================= PROJECT RECOMMENDATIONS =================

def recommend_project(skill_level="beginner", interest="general"):
    """Recommend a project based on skill level and interest."""
    projects = {
        "beginner": {
            "general": [
                "LED Blinker with Arduino - Learn basic I/O",
                "Temperature Logger - Read sensor data and display",
                "Simple Calculator in Python - Practice logic",
                "Personal Website with HTML/CSS - Learn web basics",
            ],
            "robotics": [
                "Line-following robot with IR sensors",
                "Obstacle-avoiding robot with ultrasonic sensor",
                "Bluetooth-controlled car with Arduino",
            ],
            "ai": [
                "Chatbot with if-else logic (like Diya Phase 1!)",
                "Number guessing game with learning",
                "Simple sentiment analyzer",
            ],
        },
        "intermediate": {
            "general": [
                "IoT Weather Station with ESP32 + web dashboard",
                "Home Automation system with relays and sensors",
                "REST API with Flask/FastAPI",
                "Full-stack web app with database",
            ],
            "robotics": [
                "6-DOF Robotic Arm with servo control",
                "Drone flight controller basics",
                "SLAM-based navigation robot",
            ],
            "ai": [
                "Image classifier with TensorFlow",
                "Voice assistant with speech recognition",
                "Recommendation system",
            ],
        },
        "advanced": {
            "general": [
                "Real-time operating system on ESP32",
                "Custom PCB design and manufacturing",
                "Distributed systems project",
            ],
            "robotics": [
                "Autonomous navigation with ROS2",
                "Computer vision-based object manipulation",
                "Swarm robotics coordination",
            ],
            "ai": [
                "Train a custom LLM/fine-tune a model",
                "Reinforcement learning game agent",
                "Multi-modal AI system (vision + language)",
            ],
        },
    }

    level_projects = projects.get(skill_level, projects["beginner"])
    interest_projects = level_projects.get(interest, level_projects["general"])

    result = f"Project Recommendations ({skill_level.title()} - {interest.title()}):\n\n"
    for i, p in enumerate(interest_projects, 1):
        result += f"  {i}. {p}\n"

    return result


# ================= INTENT DETECTION =================

def detect_engineering_intent(text):
    """Detect if the user needs engineering/debug help."""
    t = text.lower()

    # Voice/audio issues should be handled by conversational voice troubleshooting,
    # not engineering error analysis.
    if any(phrase in t for phrase in ["voice", "audio", "microphone", "mic", "speaker", "can't hear", "cannot hear"]):
        return None

    # Code analysis
    if "```" in text or ("analyze" in t and "code" in t) or "review my code" in t or any(p in t for p in ["fix my code", "help with code", "debug my code", "code won't run", "code not working", "won't compile", "doesn't compile", "cannot compile", "compile my code", "run my code"]):
        # Extract code between backticks if present
        code_match = re.search(r"```[\w]*\n?(.*?)```", text, re.DOTALL)
        if code_match:
            return ("analyze_code", {"code": code_match.group(1)})
        return ("analyze_error", {"error_text": text})

    if any(p in t for p in ["compile", "compilation", "build failed", "build error", "run failed"]) and any(p in t for p in ["my", "this", "the", "code", "program", "project"]):
        return ("analyze_error", {"error_text": text})

    # Hardware debugging
    if any(p in t for p in ["esp32", "arduino", "raspberry pi", "gpio", "sensor not", "motor not", "led not", "help with esp32", "help with arduino", "troubleshoot", "hardware not working"]):
        board = "esp32" if "esp" in t else "arduino" if "arduino" in t else "raspberry_pi"
        return ("hardware_debug", {"board": board, "issue": text})

    # Error analysis
    if any(p in t for p in ["error:", "traceback", "exception", "bug", "not working", "compile error", "syntax error", "runtime error", "doesn't compile", "won't compile", "cannot compile", "fails to compile"]):
        return ("analyze_error", {"error_text": text})

    # Project recommendations
    if any(p in t for p in ["recommend a project", "project idea", "what should i build", "suggest a project", "build idea", "hackathon idea"]):
        level = "beginner"
        if any(w in t for w in ["advanced", "expert", "complex"]):
            level = "advanced"
        elif any(w in t for w in ["intermediate", "medium"]):
            level = "intermediate"
        interest = "general"
        if any(w in t for w in ["robot", "robotics"]):
            interest = "robotics"
        elif any(w in t for w in ["ai", "machine learning", "ml"]):
            interest = "ai"
        return ("recommend_project", {"skill_level": level, "interest": interest})

    return None


def execute_engineering_action(action, args):
    """Execute an engineering assistant action."""
    actions = {
        "analyze_code": analyze_code,
        "analyze_error": analyze_error,
        "hardware_debug": hardware_debug,
        "recommend_project": recommend_project,
    }
    fn = actions.get(action)
    if fn:
        return fn(**args)
    return None
