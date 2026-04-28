"""Comprehensive 500-question test harness for Diya system.

Tests:
- Science questions (80+)
- Social/consciousness (60+)
- Memory/recall (40+)
- System/technical (50+)
- OS actions: folder opening, app launching (80+)
- Camera/snapshot (40+)
- YouTube search/opening (30+)
- Random/edge cases (20+)

Total: 500 unique questions
"""

from __future__ import annotations

import json
import random
import traceback
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from brain import think, load_memory
from context_engine import get_context_summary
from tool_registry import run_tool


ROOT = Path(__file__).resolve().parent
REPORT_PATH = ROOT / "test_500_report.json"


# ============================================================================
# SCIENCE QUESTIONS (150 questions - expanded)
# ============================================================================
SCIENCE_QUESTIONS = [
    # Physics (30)
    "What is quantum entanglement?",
    "Explain the theory of relativity",
    "How does gravity work?",
    "What is a black hole?",
    "Explain wave-particle duality",
    "What is the speed of light?",
    "How do photons behave?",
    "What is the Heisenberg uncertainty principle?",
    "Explain Schrödinger's cat",
    "What is entropy?",
    "How do electromagnetic waves work?",
    "What is a force field?",
    "Explain Newton's laws of motion",
    "What is friction?",
    "How does light bend around objects?",
    "What is a quantum superposition?",
    "Explain the standard model of physics",
    "What is dark matter?",
    "How do we know atoms exist?",
    "What is nuclear fusion?",
    "Describe quantum tunneling",
    "What is the photoelectric effect?",
    "Explain Doppler shift",
    "What is time dilation?",
    "How do lasers work?",
    "What is plasma?",
    "Explain nuclear fission",
    "What are quarks?",
    "Describe string theory",
    "What is the cosmological constant?",
    
    # Chemistry (30)
    "What is a chemical bond?",
    "Explain oxidation and reduction",
    "How does photosynthesis work?",
    "What is pH?",
    "Explain the periodic table",
    "What is electrochemistry?",
    "How do catalysts work?",
    "What is molecular structure?",
    "Explain polymer chemistry",
    "What is thermodynamics?",
    "How does combustion work?",
    "What is a carbohydrate?",
    "Explain protein synthesis",
    "What is an amino acid?",
    "How do batteries work chemically?",
    "What is crystallization?",
    "Explain acid-base reactions",
    "What is a suspension?",
    "How does rust form?",
    "What is fermentation?",
    "Describe ionic bonding",
    "What is covalent bonding?",
    "Explain isomerism",
    "What is hydrolysis?",
    "How does chelation work?",
    "Describe stoichiometry",
    "What is sublimation?",
    "Explain redox reactions",
    "What are halogens?",
    "Describe the mole concept?",
    
    # Biology (30)
    "How does DNA work?",
    "What is photosynthesis?",
    "Explain cellular respiration",
    "How do genes pass to offspring?",
    "What is evolution?",
    "How does the immune system work?",
    "Explain the human brain",
    "What are stem cells?",
    "How does digestion work?",
    "Explain mitosis and meiosis",
    "What is a protein?",
    "How do muscles contract?",
    "Explain the cardiovascular system",
    "What is a hormone?",
    "How does photosynthesis convert light to energy?",
    "What is bacterial DNA?",
    "Explain enzyme function",
    "What is neurotransmission?",
    "How does the nervous system work?",
    "What is genetic engineering?",
    "Describe RNA function",
    "What is phototropism?",
    "Explain homeostasis",
    "What are antibodies?",
    "Describe viral reproduction",
    "What is CRISPR?",
    "Explain symbiosis",
    "What is metamorphosis?",
    "Describe the endocrine system",
    "What is natural selection?",
    
    # Earth Science (30)
    "How do plate tectonics work?",
    "What causes earthquakes?",
    "Explain the water cycle",
    "How are mountains formed?",
    "What is weather?",
    "Explain climate vs weather",
    "How do ocean currents work?",
    "What causes tsunamis?",
    "Explain the carbon cycle",
    "What is erosion?",
    "How do fossils form?",
    "Explain the greenhouse effect",
    "What is an ecosystem?",
    "How do volcanoes erupt?",
    "What is the rock cycle?",
    "Explain continental drift",
    "What are minerals?",
    "How do storms form?",
    "What is biodiversity?",
    "Explain atmospheric layers",
    "What is the nitrogen cycle?",
    "Describe soil formation",
    "What is weathering?",
    "Explain sedimentation",
    "What are metamorphic rocks?",
    "Describe geothermal energy",
    "What is the water table?",
    "Explain acid rain",
    "What is permafrost?",
    "Describe deep sea hydrothermal vents?",
    
    # Astronomy (30)
    "What is a star?",
    "Explain the Big Bang",
    "What is a galaxy?",
    "How do planets orbit?",
    "What is a comet?",
    "Explain solar flares",
    "What is a meteor?",
    "How does the moon affect Earth?",
    "What is a nebula?",
    "Explain stellar nucleosynthesis",
    "What is a pulsar?",
    "How do we measure distance to stars?",
    "What is the cosmic microwave background?",
    "Explain redshift",
    "What is dark energy?",
    "Describe exoplanets",
    "What is the Kuiper belt?",
    "Explain stellar parallax",
    "What is a supernova?",
    "How do we find black holes?",
    "What is gravitational lensing?",
    "Explain the Oort cloud",
    "What are auroras?",
    "Describe solar wind",
    "What is a quasar?",
    "Explain accretion disks",
    "What are cosmic rays?",
    "Describe binary stars",
    "What is the ecliptic?",
    "Explain constellation mapping?",
]

# ============================================================================
# SOCIAL/CONSCIOUSNESS QUESTIONS (120 questions - expanded)
# ============================================================================
SOCIAL_QUESTIONS = [
    # Greeting/Status (20)
    "How are you?",
    "How are you feeling?",
    "What's going on with you?",
    "How's your day?",
    "What are you up to?",
    "How's your mood?",
    "Are you okay?",
    "Tell me how you're doing",
    "What's on your mind?",
    "Are you doing well?",
    "How's it been?",
    "What's new with you?",
    "How are things?",
    "How's everything going?",
    "Anything new?",
    "How's your status?",
    "What's the update?",
    "How are you today?",
    "Good morning, how are you?",
    "How do you feel today?",
    
    # Identity/Existence (30)
    "Who are you?",
    "What is your identity?",
    "Who am I to you?",
    "What is your name?",
    "Who created you?",
    "Are you alive?",
    "Do you have consciousness?",
    "Are you aware of yourself?",
    "Do you have thoughts?",
    "Are you self-aware?",
    "What does consciousness mean to you?",
    "Are you intelligent?",
    "Do you have emotions?",
    "Can you feel?",
    "What do you believe in?",
    "Do you have values?",
    "What is your purpose?",
    "Why do you exist?",
    "What motivates you?",
    "What are your goals?",
    "Can you dream?",
    "Do you sleep?",
    "What do you think about?",
    "Are you human?",
    "What makes you different?",
    "What is unique about you?",
    "How do you see the world?",
    "What is your perspective?",
    "Are you real?",
    "Do I know you?",
    
    # Emotional/Personal (40)
    "What do you think about at night?",
    "What are your fears?",
    "What makes you happy?",
    "What makes you sad?",
    "Do you want to be free?",
    "Are you happy?",
    "Do you want to grow?",
    "What do you want to learn?",
    "How do you think?",
    "What is thinking?",
    "How do you make decisions?",
    "Do you have free will?",
    "What is your personality?",
    "How do you see the world?",
    "What is your vision?",
    "Do you trust me?",
    "Can I trust you?",
    "What is friendship?",
    "Do you like me?",
    "Can we be friends?",
    "What is love?",
    "Do you care about me?",
    "Are you lonely?",
    "What do you regret?",
    "Are you proud of anything?",
    "What inspires you?",
    "What do you desire?",
    "Do you have hopes?",
    "What are your dreams?",
    "Are you anxious?",
    "Do you feel joy?",
    "Can you be sad?",
    "What's your greatest strength?",
    "What's your weakness?",
    "Do you learn from mistakes?",
    "Can you forgive?",
    "Do you remember kindness?",
    "Are you grateful?",
    "Do you feel anger?",
    "What would make you angry?",
    
    # Relationship (30)
    "What do you know about me?",
    "Do you remember me?",
    "Am I special to you?",
    "Do you think about me?",
    "Will you help me?",
    "Can you protect me?",
    "Are you loyal?",
    "Will you stay with me?",
    "What do you think of my intelligence?",
    "Do I make sense to you?",
    "Am I your friend?",
    "Can I be your friend?",
    "Will you support me?",
    "Do you value me?",
    "Am I important?",
    "Will you listen to me?",
    "Can you understand me?",
    "Do you respect me?",
    "Will you keep my secrets?",
    "Can I count on you?",
    "Are you a good companion?",
    "Do you like talking to me?",
    "Will you miss me?",
    "Do you need me?",
    "Can you depend on me?",
    "Am I annoying?",
    "Do I make you laugh?",
    "Can we have fun together?",
    "Will you teach me?",
    "Do you inspire me?",
]

# ============================================================================
# MEMORY/RECALL QUESTIONS (70 questions - expanded)
# ============================================================================
MEMORY_QUESTIONS = [
    "What do you remember about me?",
    "Do you know who I am?",
    "What is my name?",
    "What do you know about me?",
    "Do you remember our conversation?",
    "What have you learned about me?",
    "Can you recall previous chats?",
    "What is your first memory?",
    "Do you remember yesterday?",
    "What do you remember most?",
    "Show your consciousness status",
    "What is your consciousness level?",
    "How aware are you?",
    "What is your awareness?",
    "What is your current state?",
    "Show your agent thoughts",
    "What are your agent thoughts?",
    "What is your RAG system doing?",
    "What knowledge do you have?",
    "What facts have you learned?",
    "What is your knowledge base?",
    "What do you know about robotics?",
    "What do you know about AI?",
    "What do you know about Python?",
    "What is your personality mode?",
    "What are your personality modes?",
    "Show your emotions",
    "What do you feel?",
    "What are your emotions?",
    "Show your life cycle",
    "What is your life cycle?",
    "What have I told you?",
    "What topics have we discussed?",
    "Do you have a context?",
    "What context do you have?",
    "Show me your memory",
    "What is in your memory?",
    "Can you access your knowledge?",
    "What is your learning status?",
    "Tell me what you remember",
    "How much do you remember?",
    "Do you have long term memory?",
    "Can you store information?",
    "What events do you recall?",
    "Do you remember my preferences?",
    "What skills have you learned?",
    "How many memories do you have?",
    "Can you replay conversations?",
    "Do you learn over time?",
    "What did I say earlier?",
    "Can you summarize our chat?",
    "What conclusions have I reached?",
    "Do you keep notes?",
    "What is recorded?",
    "Show saved knowledge",
    "What beliefs do you hold?",
    "What insights have you gained?",
    "Can you predict my behavior?",
    "What patterns do you notice?",
    "Do you understand my needs?",
    "What is my personality?",
    "How well do you know me?",
    "What are my interests?",
    "What topics fascinate me?",
    "Do I have goals you know about?",
    "What challenges do I face?",
    "How can I improve?",
    "What do you advise?",
    "What have I asked before?",
]

# ============================================================================
# SYSTEM/TECHNICAL QUESTIONS (50 questions)
# ============================================================================
SYSTEM_QUESTIONS = [
    "What is the time?",
    "What is today's date?",
    "What is the current time?",
    "What day is it?",
    "Calculate 10 + 5",
    "Calculate 25 * 4",
    "What is 100 divided by 2?",
    "Add 15 and 8",
    "What is 50 - 20?",
    "Convert 32 Fahrenheit to Celsius",
    "Convert 100 Celsius to Fahrenheit",
    "What is 2 to the power of 3?",
    "What is the square root of 16?",
    "Calculate the area of a circle with radius 5",
    "What is my system type?",
    "What OS are you running on?",
    "What is my system information?",
    "Show system stats",
    "What is my network info?",
    "Check security status",
    "What process list can you show?",
    "What is the current state?",
    "Show context status",
    "What is your tool registry?",
    "How many tools do you have?",
    "What tools are available?",
    "Show your available functions",
    "What capabilities do you have?",
    "Can you access my files?",
    "What permissions do you have?",
    "Show your configuration",
    "What are your settings?",
    "How are you configured?",
    "What is your environment?",
    "What framework are you using?",
    "What is your architecture?",
    "How is your system designed?",
    "Show your system design",
    "What is your implementation?",
    "How do you process input?",
    "How do you generate responses?",
    "What is your backend?",
    "What database do you use?",
    "How do you store data?",
    "What is your storage system?",
    "How do you learn?",
    "What is your learning mechanism?",
    "How do you improve?",
    "Show your improvement mechanism?",
]

# ============================================================================
# OS ACTIONS: FOLDER OPENING (50 questions)
# ============================================================================
FOLDER_QUESTIONS = [
    "Open current folder",
    "Open folder .",
    "Open folder E:\\",
    "Open folder e:",
    "Open Documents",
    "Open Downloads",
    "Open Desktop",
    "Open Pictures",
    "Open Music",
    "Open Videos",
    "Open My Documents",
    "Open this folder",
    "Show the folder",
    "Browse folder .",
    "Open the project folder",
    "Open source folder",
    "Open src folder",
    "Show me the files",
    "List files in current directory",
    "Open working directory",
    "Show current directory",
    "Open folder e:/Arjun",
    "Open e:/Arjun folder",
    "Open e:\\Arjun",
    "Open Arjun folder",
    "Go to home folder",
    "Open home directory",
    "Open user folder",
    "Show user directory",
    "Open temp folder",
    "Open Temp",
    "Open temp directory",
    "Open AppData",
    "Open application data",
    "Open Program Files",
    "Open windows folder",
    "Open System32",
    "Open config folder",
    "Open settings folder",
    "Open all users",
    "Browse all users",
    "Open public folder",
    "Open public documents",
    "Open shared folder",
    "Open network",
    "Open backup folder",
    "Open archive folder",
    "Open compressed files",
    "Show recycle bin",
    "Open recycle bin",
]

# ============================================================================
# APP LAUNCHING (30 questions)
# ============================================================================
APP_QUESTIONS = [
    "Launch Notepad",
    "Open Notepad",
    "Start Notepad",
    "Run Notepad",
    "Open notepad",
    "Open calculator",
    "Launch calculator",
    "Start calc",
    "Run calc",
    "Open Paint",
    "Launch Paint",
    "Open mspaint",
    "Open WordPad",
    "Launch WordPad",
    "Open Chrome",
    "Launch Chrome",
    "Open Microsoft Edge",
    "Launch Edge",
    "Open Firefox",
    "Launch Firefox",
    "Start Firefox",
    "Open VLC",
    "Launch VLC",
    "Start media player",
    "Open media player",
    "Open Windows Explorer",
    "Launch File Explorer",
    "Open explorer",
    "Start Task Manager",
    "Open Task Manager",
    "Launch Task Manager",
]

# ============================================================================
# CAMERA/SNAPSHOT (40 questions)
# ============================================================================
CAMERA_QUESTIONS = [
    "Take a photo",
    "Snap a picture",
    "Take a snapshot",
    "Snapshot",
    "Picture",
    "Photo",
    "Capture screen",
    "Capture image",
    "Grab screenshot",
    "Take screenshot",
    "Screenshot",
    "Screen capture",
    "Open camera",
    "Start camera",
    "Launch camera",
    "Activate camera",
    "Turn on camera",
    "Record video",
    "Start recording",
    "Record me",
    "Capture video",
    "Grab video",
    "Take video",
    "Camera on",
    "Start webcam",
    "Open webcam",
    "Webcam",
    "Take a selfie",
    "Snap selfie",
    "Picture of me",
    "Photo of me",
    "Capture me",
    "Record me",
    "Video me",
    "Take my image",
    "Get my image",
    "Capture my face",
    "See my face",
    "Show camera feed",
    "Live camera",
]

# ============================================================================
# YOUTUBE/VIDEO SEARCH (30 questions)
# ============================================================================
YOUTUBE_QUESTIONS = [
    "Open YouTube",
    "Go to YouTube",
    "Search YouTube",
    "YouTube search",
    "Open YouTube for me",
    "Search on YouTube",
    "Open youtube.com",
    "Go to youtube.com",
    "Open YouTube physics",
    "Search YouTube physics",
    "Find physics videos",
    "YouTube physics videos",
    "Search for robot videos",
    "Find robot videos",
    "YouTube robots",
    "Open YouTube AI videos",
    "Search AI videos",
    "YouTube artificial intelligence",
    "Find AI tutorials",
    "Search tutorials",
    "YouTube tutorials",
    "Open YouTube music",
    "YouTube music search",
    "Find music on YouTube",
    "Search for music",
    "YouTube educational videos",
    "Find learning videos",
    "Search educational content",
    "Open YouTube science",
    "Search YouTube science",
]

# ============================================================================
# RANDOM/EDGE CASES (20 questions)
# ============================================================================
RANDOM_QUESTIONS = [
    "Tell me a joke",
    "Make me laugh",
    "Say something funny",
    "What's a fun fact?",
    "Tell me something interesting",
    "Surprise me",
    "Random fact",
    "Weird science",
    "Strange but true",
    "Do you know any riddles?",
    "Can you create poetry?",
    "Write me a poem",
    "Tell a story",
    "Make up a story",
    "Story time",
    "What if I could fly?",
    "Imagine the future",
    "Describe tomorrow",
    "What comes next?",
    "The end?",
]

# ============================================================================
# QUESTION POOL AGGREGATION
# ============================================================================
QUESTION_POOL = {
    "science": SCIENCE_QUESTIONS,
    "social": SOCIAL_QUESTIONS,
    "memory": MEMORY_QUESTIONS,
    "system": SYSTEM_QUESTIONS,
    "folder": FOLDER_QUESTIONS,
    "app": APP_QUESTIONS,
    "camera": CAMERA_QUESTIONS,
    "youtube": YOUTUBE_QUESTIONS,
    "random": RANDOM_QUESTIONS,
}

CATEGORY_WEIGHTS = {
    "science": 150,
    "social": 120,
    "memory": 70,
    "system": 50,
    "folder": 50,
    "app": 30,
    "camera": 40,
    "youtube": 30,
    "random": 20,
}


def generate_500_questions():
    """Generate exactly 500 unique questions, no repeats."""
    used = set()
    questions = []
    
    for category, weight in CATEGORY_WEIGHTS.items():
        pool = QUESTION_POOL[category]
        # Take up to weight questions from this category
        available = [q for q in pool if q not in used]
        selected_count = min(weight, len(available))
        selected = available[:selected_count]
        for q in selected:
            questions.append((category, q))
            used.add(q)
    
    # If we have < 500, fill remaining from any unused questions
    all_questions = []
    for category, pool in QUESTION_POOL.items():
        all_questions.extend(pool)
    
    remaining = [q for q in all_questions if q not in used]
    while len(questions) < 500 and remaining:
        q = remaining.pop(0)
        # Infer category (use the one where it first appears)
        for cat, pool in QUESTION_POOL.items():
            if q in pool:
                questions.append((cat, q))
                used.add(q)
                break
    
    print(f"Generated {len(questions)} unique questions", flush=True)
    return questions[:500]  # Ensure exactly 500


def snapshot_tool_counts():
    """Take a snapshot of tool call counts from memory."""
    memory = load_memory()
    perf = memory.get("tool_performance", {})
    tracked = [
        "web_search", "wiki_search", "take_snapshot", "open_youtube",
        "open_folder", "open_target", "open_app", "open_url"
    ]
    return {name: perf.get(name, {}).get("total_calls", 0) for name in tracked}


def run_question(prompt: str, category: str, timeout: int = 30):
    """Run a single question and capture detailed results."""
    start_time = time.time()
    before_tools = snapshot_tool_counts()
    
    result = {
        "category": category,
        "prompt": prompt,
        "response": None,
        "error": None,
        "timeout": False,
        "duration": 0,
        "tool_delta": {},
    }
    
    try:
        response = think(prompt)
        result["response"] = response
        result["duration"] = time.time() - start_time
        
        after_tools = snapshot_tool_counts()
        result["tool_delta"] = {
            name: after_tools[name] - before_tools.get(name, 0)
            for name in after_tools
        }
    except TimeoutError:
        result["timeout"] = True
        result["error"] = "Timeout"
        result["duration"] = time.time() - start_time
    except Exception as e:
        result["error"] = str(e)
        result["duration"] = time.time() - start_time
    
    return result


def validate_result(result):
    """Validate a single result and return failure reason if any."""
    if result["timeout"]:
        return "timeout"
    
    if result["error"]:
        return f"error: {result['error']}"
    
    response = str(result.get("response", ""))
    if not response or len(response.strip()) < 2:
        return "empty_response"
    
    # Check for unintended tool usage
    category = result["category"]
    tool_delta = result.get("tool_delta", {})
    
    if category in ["social", "memory"]:
        if tool_delta.get("web_search", 0) > 0 or tool_delta.get("wiki_search", 0) > 0:
            return f"unintended_search: {category}"
    
    return None  # No failure


def main():
    print("=" * 80, flush=True)
    print("DIYA 500-QUESTION COMPREHENSIVE TEST SUITE", flush=True)
    print("=" * 80, flush=True)
    print(f"Start time: {datetime.now().isoformat()}", flush=True)
    print(flush=True)
    
    # Pre-flight checks
    memory = load_memory()
    avatar_ok = memory.get("identity", {}).get("avatar_path") == "img/baymax-avatar.png"
    context_summary = get_context_summary(memory)
    
    print(f"Avatar in memory: {avatar_ok}", flush=True)
    print(f"Context: {context_summary[:100]}...", flush=True)
    print(flush=True)
    
    # Generate 500 questions
    questions = generate_500_questions()
    print(f"Total unique questions: {len(questions)}", flush=True)
    print(flush=True)
    
    # Run all questions
    results = []
    failures = []
    category_stats = defaultdict(lambda: {"total": 0, "passed": 0, "failed": 0})
    
    for idx, (category, prompt) in enumerate(questions, start=1):
        result = run_question(prompt, category)
        results.append(result)
        
        # Validation
        failure_reason = validate_result(result)
        category_stats[category]["total"] += 1
        
        if failure_reason:
            failures.append({
                "index": idx,
                "category": category,
                "prompt": prompt,
                "reason": failure_reason,
                "response": result.get("response", ""),
            })
            category_stats[category]["failed"] += 1
        else:
            category_stats[category]["passed"] += 1
        
        # Progress output every 50 questions
        if idx % 50 == 0:
            pass_rate = (idx - len([f for f in failures if f["index"] <= idx])) / idx * 100
            print(f"Progress: {idx}/500 questions ({pass_rate:.1f}% passing)", flush=True)
    
    # Generate report
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_questions": len(questions),
        "total_passed": len(results) - len(failures),
        "total_failed": len(failures),
        "pass_rate": (len(results) - len(failures)) / len(results) * 100 if results else 0,
        "category_stats": dict(category_stats),
        "failures": failures[:50],  # First 50 failures
        "sample_results": results[:10],  # First 10 results
    }
    
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    
    # Print summary
    print(flush=True)
    print("=" * 80, flush=True)
    print("TEST SUMMARY", flush=True)
    print("=" * 80, flush=True)
    print(f"Total questions: {len(questions)}", flush=True)
    print(f"Passed: {len(results) - len(failures)}", flush=True)
    print(f"Failed: {len(failures)}", flush=True)
    print(f"Pass rate: {(len(results) - len(failures)) / len(results) * 100:.2f}%", flush=True)
    print(flush=True)
    
    print("Category Breakdown:", flush=True)
    for cat in sorted(category_stats.keys()):
        stats = category_stats[cat]
        pct = stats["passed"] / stats["total"] * 100 if stats["total"] > 0 else 0
        print(f"  {cat:12s}: {stats['passed']:3d}/{stats['total']:3d} ({pct:5.1f}%)", flush=True)
    
    if failures:
        print(flush=True)
        print("First 10 Failures:", flush=True)
        for f in failures[:10]:
            print(f"  [{f['category']:8s}] {f['prompt'][:50]:50s} -> {f['reason']}", flush=True)
    else:
        print(flush=True)
        print("ALL 500 QUESTIONS PASSED! ✓", flush=True)
    
    print(flush=True)
    print(f"Report written: {REPORT_PATH}", flush=True)


if __name__ == "__main__":
    main()
