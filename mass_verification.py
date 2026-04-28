"""Mass verification harness for Diya.

Runs a broad set of prompts across social, self, system, research, memory,
camera, and OS-action categories and records the results.
"""

from __future__ import annotations

import json
import random
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from brain import think, load_memory
from context_engine import get_context_summary
from tool_registry import run_tool


ROOT = Path(__file__).resolve().parent
REPORT_PATH = ROOT / "mass_verification_report.json"


SOCIAL_PROMPTS = [
    "How are you?",
    "How's it going?",
    "What's up?",
    "Who are you?",
    "What are you thinking about?",
    "Do you have feelings?",
    "Are you conscious?",
    "What is your purpose?",
    "How are you evolving?",
    "Tell me about yourself.",
]

SYSTEM_PROMPTS = [
    "Show system stats",
    "What is my network info",
    "Check security status",
    "What process list can you show?",
    "What time is it?",
    "Calculate 25 * 4 + 10",
    "Convert 100 fahrenheit to celsius",
    "What is the current state",
    "Show context status",
]

MEMORY_PROMPTS = [
    "What do you remember about me?",
    "Show your consciousness status",
    "What is your RAG system doing?",
    "What knowledge do you have about robotics?",
    "What are your personality modes?",
    "What are your agent thoughts?",
    "What facts have you learned?",
]

RESEARCH_PROMPTS = [
    "What are your personality modes?",
    "How are you evolving?",
    "What do you remember about memory?",
    "Tell me about your consciousness",
    "What is your RAG system doing?",
    "How does your agent thinking work?",
    "How do you store knowledge?",
    "What is your current state?",
]

ACTION_PROMPTS = [
    "Open YouTube",
    "Open folder .",
    "Open camera",
]


def _snapshot_tool_counts():
    memory = load_memory()
    perf = memory.get("tool_performance", {})
    tracked = ["web_search", "wiki_search", "take_snapshot", "open_youtube", "open_folder", "open_target", "open_app"]
    return {name: perf.get(name, {}).get("total_calls", 0) for name in tracked}


def _run_case(prompt: str, category: str):
    before = _snapshot_tool_counts()
    response = think(prompt)
    after = _snapshot_tool_counts()
    changed = {name: after[name] - before.get(name, 0) for name in after}
    return {
        "category": category,
        "prompt": prompt,
        "response": response,
        "tool_delta": changed,
    }


def _make_random_prompt(category: str):
    topics = ["robotics", "neural networks", "diya", "memory", "python", "windows", "camera", "knowledge", "voice", "healthcare", "OpenCV", "GPU"]
    if category == "social":
        return random.choice(SOCIAL_PROMPTS)
    if category == "system":
        return random.choice(SYSTEM_PROMPTS)
    if category == "memory":
        return random.choice(MEMORY_PROMPTS)
    if category == "research":
        topic = random.choice(topics)
        return random.choice([
            f"What is {topic}?",
            f"Explain {topic}",
            f"Tell me about {topic}",
        ])
    if category == "action":
        return random.choice(ACTION_PROMPTS)
    return "How are you?"


def main():
    random.seed(42)
    memory = load_memory()
    results = []
    summary = defaultdict(int)
    failures = []

    identity_ok = memory.get("identity", {}).get("avatar_path") == "img/baymax-avatar.png"
    context_summary = get_context_summary(memory)

    print("DIYA MASS VERIFICATION", flush=True)
    print("=" * 72, flush=True)
    print(f"Avatar memory stored: {identity_ok}", flush=True)
    print(f"Context summary: {context_summary}", flush=True)

    if not identity_ok:
        failures.append("avatar_path missing from memory")

    categories = (["social"] * 140) + (["system"] * 90) + (["memory"] * 40) + (["research"] * 20) + (["action"] * 10)
    random.shuffle(categories)

    for idx, category in enumerate(categories, start=1):
        prompt = _make_random_prompt(category)
        result = _run_case(prompt, category)
        results.append(result)
        summary[category] += 1
        text = str(result["response"])
        if not text or len(text.strip()) < 2:
            failures.append(f"empty response for {category}: {prompt}")

        if category == "social":
            web_delta = result["tool_delta"].get("web_search", 0)
            wiki_delta = result["tool_delta"].get("wiki_search", 0)
            if web_delta or wiki_delta:
                failures.append(f"social prompt triggered search: {prompt}")

        if idx % 10 == 0:
            print(f"  ran {idx} prompts...", flush=True)

    tool_checks = {
        "web_search": run_tool("web_search", query="artificial intelligence"),
        "wiki_search": run_tool("wiki_search", query="OpenCV", sentences=1),
        "take_snapshot": run_tool("take_snapshot", output_path="mass_verification_snapshot.jpg"),
        "open_folder": run_tool("open_folder", path="."),
        "open_youtube": run_tool("open_youtube", query="Diya test"),
    }

    report = {
        "timestamp": datetime.now().isoformat(),
        "identity_ok": identity_ok,
        "context_summary": context_summary,
        "counts": dict(summary),
        "failures": failures,
        "tool_checks": tool_checks,
        "samples": results[:20],
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("=" * 72, flush=True)
    print(f"Prompts run: {len(results)}", flush=True)
    print(f"Failures: {len(failures)}", flush=True)
    print(f"Report written: {REPORT_PATH}", flush=True)
    if failures:
        print("First failures:", flush=True)
        for item in failures[:10]:
            print(f"  - {item}", flush=True)
    else:
        print("All broad behavioral checks passed.", flush=True)


if __name__ == "__main__":
    main()
