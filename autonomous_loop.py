"""
autonomous_loop.py — Diya's Autonomous Conversation Engine

Runs as a background thread. Every tick, Diya's inner life advances:
she thinks, reflects, dreams, and sometimes speaks on her own.
"""

import threading
import time
import random
from datetime import datetime

from brain import think, load_memory, save_memory
from self_evolution import run_evolution_cycle, choose_autonomous_objective, execute_autonomous_objective
from consciousness_engine import consciousness_engine
from personality_modes import choose_best_mode
from life_cycle import (
    get_current_state,
    get_state_properties,
    get_energy_level,
    get_tick_interval,
    should_speak,
    generate_idle_thought,
    generate_dream,
    get_wakeup_message,
    get_sleep_message,
)
from self_learning import start_self_learning


class DiyaAutonomousLoop:
    """Background thread that runs Diya's autonomous life."""

    def __init__(self, print_fn=None):
        self._running = False
        self._thread = None
        self._lock = threading.Lock()
        self._paused = False
        self._last_spoke_time = time.time()
        self._last_user_time = None
        self._previous_state = None
        self._print_fn = print_fn or self._default_print
        self._sleep_announced = False
        self._wake_announced = False

    # ---------- PUBLIC API ----------

    def start(self):
        """Start the autonomous loop in a background daemon thread."""
        self._running = True
        self._previous_state = get_current_state()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        # Also start self-learning system
        start_self_learning()

    def stop(self):
        """Stop the autonomous loop."""
        self._running = False

    def pause(self):
        """Temporarily pause autonomous speech (e.g. while processing user input)."""
        self._paused = True

    def resume(self):
        """Resume autonomous speech."""
        self._paused = False

    def notify_user_interaction(self):
        """Call this whenever the user sends a message."""
        self._last_user_time = time.time()

    def set_wake_announced(self, state=True):
        """Manually set whether the wake-up message has been announced."""
        self._wake_announced = state
        if state:
            self._sleep_announced = False

    # ---------- INTERNAL ----------

    def _default_print(self, message):
        """Default print with timestamp and Diya prefix."""
        timestamp = datetime.now().strftime("%H:%M")
        # Encode safely for Windows terminals
        safe_msg = message.encode("ascii", "replace").decode()
        print(f"\n[{timestamp}] Diya: {safe_msg}")

    def _loop(self):
        """Main autonomous loop — runs forever in background."""
        while self._running:
            try:
                self._tick()
            except Exception as e:
                # Never crash the background loop - log to a file for diagnostics
                try:
                    with open("autonomous_errors.log", "a") as f:
                        f.write(f"[{datetime.now()}] Loop error: {str(e)}\n")
                except:
                    pass
                time.sleep(5) # Wait a bit before retrying if there's a crash

            # Wait for next tick (randomized interval based on state)
            interval = get_tick_interval()
            time.sleep(interval)

    def _tick(self):
        """Single tick of Diya's autonomous life."""
        if self._paused:
            return

        current_state = get_current_state()
        memory = load_memory()

        # Advance consciousness
        consciousness_engine.process_consciousness(memory)

        # Ensure life_cycle exists in memory
        if "life_cycle" not in memory:
            memory["life_cycle"] = {
                "current_state": current_state,
                "energy": get_energy_level(),
                "last_sleep_time": None,
                "last_wake_time": None,
                "dreams": [],
                "daily_journal": [],
                "idle_thoughts": [],
                "last_spoke_at": None,
                "last_user_interaction": None,
            }

        lc = memory["life_cycle"]
        lc["current_state"] = current_state
        lc["energy"] = get_energy_level()

        # ---------- STATE TRANSITIONS ----------
        self._handle_transitions(current_state, memory)

        # ---------- STATE-SPECIFIC BEHAVIOR ----------
        if current_state == "sleeping":
            self._handle_sleep(memory)
        else:
            self._handle_awake(current_state, memory)

        # Update previous state
        self._previous_state = current_state

        # Save
        save_memory(memory)

    def _handle_transitions(self, current_state, memory):
        """Handle transitions between life states (sleep/wake boundaries)."""
        lc = memory["life_cycle"]

        # Just woke up
        if self._previous_state == "sleeping" and current_state != "sleeping":
            if not self._wake_announced:
                lc["last_wake_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                msg = get_wakeup_message(memory)
                self._speak(msg)
                self._wake_announced = True
                self._sleep_announced = False

                # Add to daily journal
                lc["daily_journal"].append({
                    "time": datetime.now().strftime("%H:%M"),
                    "event": "woke_up",
                    "note": "Starting a new day"
                })

        # Just fell asleep
        elif self._previous_state != "sleeping" and current_state == "sleeping":
            if not self._sleep_announced:
                lc["last_sleep_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                msg = get_sleep_message()
                self._speak(msg)
                self._sleep_announced = True
                self._wake_announced = False

                # Add to daily journal
                lc["daily_journal"].append({
                    "time": datetime.now().strftime("%H:%M"),
                    "event": "fell_asleep",
                    "note": "Ending the day"
                })

        # State changed (but not sleep/wake boundary)
        elif self._previous_state != current_state:
            state_messages = {
                "active": "I feel my energy rising. This is going to be a good stretch.",
                "lunch_break": "Time for a little break. Even I need to slow down sometimes.",
                "afternoon": "Alright, back to deep thinking mode.",
                "evening": "The day is winding down. I feel more reflective now.",
                "night": "It is getting late. I should start winding down.",
                "sleepy": "*yawns* I am getting really tired...",
            }
            if current_state in state_messages:
                # Only announce state changes sometimes (not every time)
                if random.random() < 0.6:
                    self._speak(state_messages[current_state])

    def _handle_sleep(self, memory):
        """Handle sleeping state — generate dreams, consolidate memories."""
        lc = memory["life_cycle"]

        # Generate a dream every few ticks
        if random.random() < 0.3:
            dream = generate_dream(memory)
            lc["dreams"].append(dream)
            # Keep only last 10 dreams
            lc["dreams"] = lc["dreams"][-10:]

        # Consolidate daily journal (keep last 20 entries)
        lc["daily_journal"] = lc["daily_journal"][-20:]

    def _handle_awake(self, current_state, memory):
        """Handle awake states — decide whether to speak, think, etc."""
        lc = memory["life_cycle"]
        now = time.time()

        # Reflect quietly on every awake tick so the agent can adjust its own priorities.
        run_evolution_cycle(memory)

        # Let the brain steer its own mode while idle.
        selected_mode = choose_best_mode("", memory, memory.get("context", {}))
        if selected_mode and selected_mode != memory.get("personality_mode", {}).get("current"):
            memory.setdefault("personality_mode", {})["current"] = selected_mode
            memory["personality_mode"].setdefault("history", []).append(selected_mode)
            memory["personality_mode"]["history"] = memory["personality_mode"]["history"][-20:]

        # Choose a self-directed objective and execute it periodically even without user input.
        if self._last_user_time is None or (now - self._last_user_time) > 120:
            objective = choose_autonomous_objective(memory)
            note = execute_autonomous_objective(memory)
            if note:
                lc.setdefault("daily_journal", []).append({
                    "time": datetime.now().strftime("%H:%M"),
                    "event": "autonomous_objective",
                    "note": note[:120],
                })
                lc["daily_journal"] = lc["daily_journal"][-20:]
                # Only speak occasionally to avoid noise.
                if random.random() < 0.2:
                    self._speak(f"*self-directed focus* {objective['name']}")

        last_spoke_ago = now - self._last_spoke_time
        last_user_ago = None
        if self._last_user_time:
            last_user_ago = now - self._last_user_time

        # Should Diya speak on her own?
        if should_speak(last_spoke_ago, last_user_ago):
            thought = generate_idle_thought(memory)

            # Store the idle thought
            lc["idle_thoughts"].append({
                "time": datetime.now().strftime("%H:%M"),
                "thought": thought,
                "state": current_state
            })
            # Keep only last 30 idle thoughts
            lc["idle_thoughts"] = lc["idle_thoughts"][-30:]

            # Journal it
            lc["daily_journal"].append({
                "time": datetime.now().strftime("%H:%M"),
                "event": "spoke_autonomously",
                "note": thought[:80]
            })

            self._speak(thought)

    def _speak(self, message):
        """Output a message from Diya and update timing."""
        self._last_spoke_time = time.time()
        self._print_fn(message)
