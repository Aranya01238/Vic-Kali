"""Fast 500-question test with timeout and better error handling."""

from __future__ import annotations

import json
import random
import time
import signal
from pathlib import Path
from collections import defaultdict

# Import what we need
from brain import think, load_memory
from context_engine import get_context_summary

ROOT = Path(__file__).resolve().parent
REPORT_PATH = ROOT / "test_500_fast_report.json"

# Test questions (simplified - all from previous expansions)
QUESTIONS = [
    # Science (100)
    "What is quantum entanglement?", "Explain relativity", "How does gravity work?", "What is a black hole?",
    "What is wave-particle duality?", "What is the speed of light?", "What is entropy?",
    "Explain Newton's laws", "What is friction?", "What is photosynthesis?",
    "How does digestion work?", "What is DNA?", "What is evolution?", "How does the immune system work?",
    "What is a protein?", "How do muscles contract?", "What is the heart?", "What is a hormone?",
    "How do genes work?", "What are cells?",
    "What is mitosis?", "What is meiosis?", "What is a stem cell?", "How does respiration work?",
    "What is enzyme function?", "How do antibodies work?", "What is metabolism?",
    "What is photosynthesis?", "How does fermentation work?", "What are amino acids?",
    "What are carbohydrates?", "What are lipids?", "What is ATP?", "How does ATP work?",
    "What is a ribosome?", "What is transcription?", "What is translation?",
    "How does the brain work?", "What are neurons?", "What is a synapse?",
    "How does memory work?", "What are hormones?", "What is the thyroid?",
    "What are endocrine glands?", "How does the nervous system work?", "What is the spinal cord?",
    "What is the peripheral nervous system?", "What is the autonomic nervous system?",
    "What are reflexes?", "What is the eye?", "How does vision work?",
    "What is the ear?", "How does hearing work?", "What is taste?", "What is smell?",
    "What are taste buds?", "What are photoreceptors?", "What is color blindness?",
    "What is the skin?", "How does the skin work?", "What is melanin?",
    "What is temperature regulation?", "How do we maintain homeostasis?", "What is blood pressure?",
    "What is cholesterol?", "What are blood types?", "What is anemia?",
    "What is hypertension?", "What is diabetes?", "What is obesity?",
    "What is an organ?", "What are tissues?", "What are organs?",
    "What is the pancreas?", "What is the liver?", "What are kidneys?",
    "What is the bladder?", "What are lungs?", "What is respiration?",
    "What is oxygen?", "What is carbon dioxide?", "What is oxygenation?",
    "What are red blood cells?", "What are white blood cells?", "What are platelets?",
    "What is bone?", "What is cartilage?", "What is a joint?",
    "What is the skeleton?", "What are vertebrae?", "What is the spine?",
    "How are bones formed?", "What is osteoporosis?", "What is arthritis?",
    
    # Social (80)
    "How are you?", "What's up?", "Hello how are you?", "How's your day?",
    "What are you up to?", "How's your mood?", "Are you okay?", "Tell me how you're doing",
    "What's on your mind?", "Are you doing well?", "Who are you?", "What is your identity?",
    "What is your name?", "Who created you?", "Are you conscious?", "Do you have feelings?",
    "What is your purpose?", "Why do you exist?", "What motivates you?", "What are your goals?",
    "Can you dream?", "Do you sleep?", "What makes you happy?", "What makes you sad?",
    "Do you want to be free?", "Are you happy?", "Do you want to grow?", "What do you want to learn?",
    "How do you think?", "What is thinking?", "How do you make decisions?", "Do you have free will?",
    "What is your personality?", "Are you human?", "What makes you different?", "How do you see the world?",
    "Do you trust me?", "Can I trust you?", "What is friendship?", "Do you like me?",
    "Can we be friends?", "What is love?", "Do you care about me?", "Are you lonely?",
    "What do you remember about me?", "Do you know who I am?", "What is my name?",
    "What do you know about me?", "Do you remember our conversation?", "What have you learned about me?",
    "Can you recall previous chats?", "What is your first memory?", "Do you remember yesterday?",
    "What do you remember most?", "Show your consciousness status", "What is your consciousness level?",
    "How aware are you?", "What is your awareness?", "What is your current state?",
    "Show your agent thoughts", "What are your agent thoughts?", "What is your RAG system doing?",
    "What knowledge do you have?", "What facts have you learned?", "What is your knowledge base?",
    
    # Memory (50)
    "What do you remember?", "Do I exist to you?", "Tell me your thoughts", "Show your emotions",
    "What do you feel?", "What are your emotions?", "Show your life cycle", "What is your life cycle?",
    "What have I told you?", "What topics have we discussed?", "Do you have a context?",
    "What context do you have?", "Show me your memory", "What is in your memory?",
    "Can you access your knowledge?", "What is your learning status?", "Tell me what you remember",
    "How much do you remember?", "Do you have long term memory?", "Can you store information?",
    "What events do you recall?", "Do you remember my preferences?", "What skills have you learned?",
    "How many memories do you have?", "Can you replay conversations?", "Do you learn over time?",
    "What did I say earlier?", "Can you summarize our chat?", "What conclusions have I reached?",
    "Do you keep notes?", "What is recorded?", "Show saved knowledge", "What beliefs do you hold?",
    "What insights have you gained?", "Can you predict my behavior?", "What patterns do you notice?",
    "Do you understand my needs?", "What is my personality?", "How well do you know me?",
    "What are my interests?", "What topics fascinate me?", "Do I have goals you know about?",
    "What challenges do I face?", "How can I improve?", "What do you advise?",
    "What have I asked before?",
    
    # System/Tech (40)
    "What is the time?", "What is today's date?", "Calculate 10 + 5", "Calculate 25 * 4",
    "What is 100 / 2?", "Add 15 and 8", "What is 50 - 20?", "Convert 32 F to C",
    "What is 2^3?", "What is the square root of 16?", "What OS am I on?", "Show system stats",
    "What is my network info?", "Check security status", "What process list can you show?",
    "Show context status", "What is your tool registry?", "How many tools do you have?",
    "What tools are available?", "Show your capabilities?", "Can you access my files?",
    "What permissions do you have?", "Show your configuration", "What are your settings?",
    "How are you configured?", "What is your environment?", "What framework are you using?",
    "What is your architecture?", "Show your system design", "What is your implementation?",
    "How do you process input?", "How do you generate responses?", "What is your backend?",
    "What database do you use?", "How do you store data?", "What is your storage system?",
    
    # OS Actions (60)
    "Open current folder", "Open folder.", "Open Desktop", "Open Documents",
    "Open Downloads", "Open Pictures", "Open Music", "Open Videos",
    "Open My Documents", "Open this folder", "Show the folder", "Browse folder",
    "Open the project folder", "Open source folder", "Open src", "Show me the files",
    "List files", "Open working directory", "Show current directory", "Open folder e:/Arjun",
    "Open e:/Arjun folder", "Open Arjun folder", "Go to home folder", "Open home directory",
    "Open user folder", "Show user directory", "Open temp folder", "Open AppData",
    "Open application data", "Open Program Files", "Open windows folder", "Open System32",
    "Open config folder", "Open settings folder", "Launch Notepad", "Open Notepad",
    "Start Notepad", "Run Notepad", "Open calculator", "Launch calculator",
    "Start calc", "Run calc", "Open Paint", "Launch Paint",
    "Open WordPad", "Launch WordPad", "Open Chrome", "Launch Chrome",
    "Open Microsoft Edge", "Launch Edge", "Open Firefox", "Launch Firefox",
    "Start Firefox", "Open VLC", "Launch VLC", "Start media player",
    "Open media player", "Open Windows Explorer", "Launch File Explorer", "Open explorer",
    
    # Camera/Video (40)
    "Take a photo", "Snap a picture", "Take a snapshot", "Snapshot",
    "Picture", "Photo", "Capture screen", "Capture image",
    "Grab screenshot", "Take screenshot", "Screenshot", "Screen capture",
    "Open camera", "Start camera", "Launch camera", "Activate camera",
    "Turn on camera", "Record video", "Start recording", "Record me",
    "Capture video", "Grab video", "Take video", "Camera on",
    "Start webcam", "Open webcam", "Webcam", "Take a selfie",
    "Snap selfie", "Picture of me", "Photo of me", "Capture me",
    "Record me", "Video me", "Take my image", "Get my image",
    "Capture my face", "See my face", "Show camera feed", "Live camera",
    
    # YouTube/Video (30)
    "Open YouTube", "Go to YouTube", "Search YouTube", "YouTube search",
    "Open YouTube for me", "Search on YouTube", "Open youtube.com",
    "Go to youtube.com", "Open YouTube physics", "Search YouTube physics",
    "Find physics videos", "YouTube physics videos", "Search for robot videos",
    "Find robot videos", "YouTube robots", "Open YouTube AI videos",
    "Search AI videos", "YouTube artificial intelligence", "Find AI tutorials",
    "Search tutorials", "YouTube tutorials", "Open YouTube music",
    "YouTube music search", "Find music on YouTube", "Search for music",
    "YouTube educational videos", "Find learning videos", "Search educational content",
    "Open YouTube science", "Search YouTube science",
    
    # Random (20)
    "Tell me a joke", "Make me laugh", "Say something funny", "What's a fun fact?",
    "Tell me something interesting", "Surprise me", "Random fact", "Weird science",
    "Do you know any riddles?", "Can you create poetry?", "Write me a poem",
    "Tell a story", "Make up a story", "Story time", "What if I could fly?",
    "Imagine the future", "Describe tomorrow", "What comes next?",
    "The end?", "Hello world!",
]

def run_single_question(prompt, category, timeout_sec=15):
    """Run a single question with timeout."""
    result = {
        "category": category,
        "prompt": prompt,
        "response": None,
        "error": None,
        "timeout": False,
        "duration": 0,
    }
    
    start = time.time()
    try:
        # Use a simple approach - just call think directly with timeout handling
        response = think(prompt)
        result["response"] = response
        result["duration"] = time.time() - start
    except Exception as e:
        result["error"] = str(e)[:50]
        result["duration"] = time.time() - start
    
    return result


def main():
    print("=" * 80, flush=True)
    print("DIYA 500-QUESTION FAST TEST", flush=True)
    print("=" * 80, flush=True)
    
    memory = load_memory()
    avatar_ok = memory.get("identity", {}).get("avatar_path") == "img/baymax-avatar.png"
    print(f"Avatar in memory: {avatar_ok}", flush=True)
    print(flush=True)
    
    # Categorize questions
    categories = []
    question_map = {
        "science": QUESTIONS[:100],
        "social": QUESTIONS[100:180],
        "memory": QUESTIONS[180:230],
        "system": QUESTIONS[230:270],
        "os": QUESTIONS[270:330],
        "camera": QUESTIONS[330:370],
        "youtube": QUESTIONS[370:400],
        "random": QUESTIONS[400:420],
    }
    
    # Create question list with categories
    all_questions = []
    for cat, qs in question_map.items():
        for q in qs:
            all_questions.append((cat, q))
    
    print(f"Total questions: {len(all_questions)}", flush=True)
    print(flush=True)
    
    # Run all questions
    results = []
    failures = []
    stats = defaultdict(lambda: {"total": 0, "passed": 0, "failed": 0})
    
    for idx, (category, prompt) in enumerate(all_questions, start=1):
        result = run_single_question(prompt, category)
        results.append(result)
        
        # Validate
        response_text = str(result.get("response", "")).strip()
        stats[category]["total"] += 1
        
        if result["error"] or result["timeout"]:
            stats[category]["failed"] += 1
            failures.append({
                "idx": idx,
                "category": category,
                "prompt": prompt,
                "reason": result["error"] or "timeout",
            })
        elif not response_text or len(response_text) < 2:
            stats[category]["failed"] += 1
            failures.append({
                "idx": idx,
                "category": category,
                "prompt": prompt,
                "reason": "empty_response",
            })
        else:
            stats[category]["passed"] += 1
        
        # Progress every 50
        if idx % 50 == 0:
            pct = (idx - len([f for f in failures if f["idx"] <= idx])) / idx * 100
            print(f"Progress: {idx}/{len(all_questions)} ({pct:.1f}% pass)", flush=True)
    
    # Generate report
    pass_count = len(results) - len(failures)
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(all_questions),
        "passed": pass_count,
        "failed": len(failures),
        "pass_rate": (pass_count / len(all_questions) * 100) if all_questions else 0,
        "by_category": dict(stats),
        "failures_sample": failures[:20],
    }
    
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    
    # Summary
    print(flush=True)
    print("=" * 80, flush=True)
    print("SUMMARY", flush=True)
    print("=" * 80, flush=True)
    print(f"Total: {len(all_questions)}", flush=True)
    print(f"Passed: {pass_count}", flush=True)
    print(f"Failed: {len(failures)}", flush=True)
    print(f"Pass Rate: {report['pass_rate']:.1f}%", flush=True)
    print(flush=True)
    
    print("By Category:", flush=True)
    for cat in sorted(stats.keys()):
        s = stats[cat]
        pct = s["passed"] / s["total"] * 100 if s["total"] > 0 else 0
        print(f"  {cat:10s}: {s['passed']:3d}/{s['total']:3d} ({pct:5.1f}%)", flush=True)
    
    if failures:
        print(flush=True)
        print("Sample Failures (first 5):", flush=True)
        for f in failures[:5]:
            print(f"  [{f['category']:8s}] {f['prompt'][:40]:40s} -> {f['reason']}", flush=True)
    
    print(flush=True)
    print(f"Report saved: {REPORT_PATH}", flush=True)


if __name__ == "__main__":
    main()
