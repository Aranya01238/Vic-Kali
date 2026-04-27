"""self_evolution.py - guarded self-directed evolution layer for Diya.

This module does not claim consciousness. It tracks reflections, identifies
repeated failure patterns, and proposes safe adjustments to the agent's
operating priorities.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime


DEFAULT_EVOLUTION_STATE = {
    "version": 1,
    "reflection_count": 0,
    "last_reflection": None,
    "current_focus": "general_growth",
    "autonomous_objective": None,
    "active_hypotheses": [],
    "approved_changes": [],
    "recent_observations": [],
    "history": [],
}


def ensure_evolution_state(memory):
    """Make sure the evolution state exists in memory."""
    evolution = memory.setdefault("evolution", {})
    for key, value in DEFAULT_EVOLUTION_STATE.items():
        if key not in evolution:
            evolution[key] = value.copy() if isinstance(value, list) else value
    return evolution


def _safe_append(target, value, limit=12):
    if value and value not in target:
        target.append(value)
        del target[:-limit]


def _top_fallback_pattern(memory):
    conversation = memory.get("conversation", {})
    recent_responses = conversation.get("recent_responses", [])
    if not recent_responses:
        return None
    return Counter(recent_responses).most_common(1)[0][0]


def _failure_hints(memory):
    hints = []

    context = memory.get("context", {})
    if context.get("current_mood") == "confused":
        hints.append("tighten confusion detection and improve clarifying replies")

    tool_performance = memory.get("tool_performance", {})
    for tool_name, stats in tool_performance.items():
        total = stats.get("success", 0) + stats.get("fail", 0)
        if total >= 4:
            failure_rate = stats.get("fail", 0) / total
            if failure_rate > 0.4:
                hints.append(f"improve {tool_name} reliability")

    recent_response = _top_fallback_pattern(memory)
    if recent_response:
        hints.append(f"reduce repetition around: {recent_response[:48]}")

    return hints


def run_evolution_cycle(memory, text=""):
    """Record a reflection and propose the next safe growth direction."""
    evolution = ensure_evolution_state(memory)
    evolution["reflection_count"] += 1

    observations = []
    if text:
        observations.append(f"latest input: {text[:80]}")

    context = memory.get("context", {})
    if context:
        observations.append(f"mood={context.get('current_mood', 'neutral')}")
        observations.append(f"task={context.get('current_task', 'general')}")

    mode = memory.get("personality_mode", {}).get("current", "friend")
    observations.append(f"mode={mode}")

    failure_hints = _failure_hints(memory)
    observations.extend(failure_hints[:3])

    if not observations:
        observations.append("stable operating conditions")

    reflection = "; ".join(observations)
    evolution["last_reflection"] = reflection
    evolution["recent_observations"].append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "reflection": reflection,
    })
    evolution["recent_observations"] = evolution["recent_observations"][-12:]
    evolution["history"].append(reflection)
    evolution["history"] = evolution["history"][-20:]

    next_focus = "general_growth"
    if any("reliability" in item for item in failure_hints):
        next_focus = "tool_reliability"
    elif any("repetition" in item for item in failure_hints):
        next_focus = "response_variety"
    elif context.get("current_mood") in {"confused", "anxious"}:
        next_focus = "clarity_and_support"

    evolution["current_focus"] = next_focus
    _safe_append(evolution["active_hypotheses"], next_focus)

    if next_focus == "response_variety":
        approved = "rotate conversational fallback phrasing"
    elif next_focus == "tool_reliability":
        approved = "prefer higher-confidence tools and clearer routing"
    elif next_focus == "clarity_and_support":
        approved = "use calmer, more explicit explanations"
    else:
        approved = "maintain broad learning and reflection"

    _safe_append(evolution["approved_changes"], approved)
    return {
        "focus": next_focus,
        "reflection": reflection,
        "approved_change": approved,
    }


def choose_autonomous_objective(memory):
    """Select one safe objective the agent can work on without user input."""
    evolution = ensure_evolution_state(memory)
    focus = evolution.get("current_focus", "general_growth")

    if focus == "response_variety":
        objective = {
            "name": "diversify conversational replies",
            "reason": "reduce repeated fallback phrasing",
            "action": "rotate from a broader reply bank and avoid recent wording",
        }
    elif focus == "tool_reliability":
        objective = {
            "name": "inspect tool reliability",
            "reason": "high failure rates need attention",
            "action": "favor higher-confidence tools and avoid low-confidence routes",
        }
    elif focus == "clarity_and_support":
        objective = {
            "name": "clarify responses",
            "reason": "user state suggests confusion or anxiety",
            "action": "prefer direct, stepwise explanations",
        }
    else:
        objective = {
            "name": "review current memory and goals",
            "reason": "maintain continuous self-direction",
            "action": "review conversation state, goals, and recent changes",
        }

    evolution["autonomous_objective"] = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **objective,
    }
    return evolution["autonomous_objective"]


def execute_autonomous_objective(memory):
    """Perform a safe autonomous update based on the selected objective."""
    evolution = ensure_evolution_state(memory)
    objective = evolution.get("autonomous_objective") or choose_autonomous_objective(memory)

    if not objective:
        return None

    note = (
        f"autonomous objective: {objective['name']} | "
        f"reason: {objective['reason']} | action: {objective['action']}"
    )
    _safe_append(evolution["history"], note, limit=20)
    _safe_append(evolution["recent_observations"], {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "reflection": note,
    }, limit=12)

    approved = f"work on {objective['name']}"
    _safe_append(evolution["approved_changes"], approved)
    evolution["last_reflection"] = note
    return note


def evolution_summary(memory):
    """Generate a compact status summary for the user."""
    evolution = ensure_evolution_state(memory)
    focus = evolution.get("current_focus", "general_growth")
    reflection_count = evolution.get("reflection_count", 0)
    approved = evolution.get("approved_changes", [])
    last_change = approved[-1] if approved else "none"
    return (
        f"Evolution focus: {focus} | reflections: {reflection_count} | "
        f"last approved change: {last_change}"
    )
