"""
main.py - Diya: The Autonomous AI Healthcare Companion

Diya lives, breathes, thinks, and speaks on her own.
She has personality modes, voice support, task management,
engineering assistance, and a full circadian rhythm.

Usage: python main.py
       python main.py --voice   (enable voice mode)
"""

import sys
import time
from datetime import datetime

from brain import think, load_memory, save_memory
from life_cycle import get_current_state, get_state_properties, get_wakeup_message, wake_up_manually
from autonomous_loop import DiyaAutonomousLoop
from personality_modes import get_mode_info, list_modes
from context_engine import get_context_summary
import queue
from voice_system import (
    speak,
    speak_blocking,
    stop_speaking,
    is_tts_available,
    is_stt_available,
    listen,
    listen_continuous,
    detect_wake_word,
    strip_wake_word,
    get_voice_status,
    get_tts_diagnostics,
)


# ================= SAFE PRINT =================

def safe_print(message):
    """Print safely on Windows terminals."""
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode("ascii", "replace").decode())


def diya_print(message):
    """Print a message from Diya with timestamp."""
    timestamp = datetime.now().strftime("%H:%M")
    safe_print(f"\n[{timestamp}] Diya: {message}")


# ================= VOICE MODE =================

_voice_enabled = False
_tts_enabled = False


def toggle_voice():
    """Toggle voice input/output."""
    global _voice_enabled, _tts_enabled
    _voice_enabled = not _voice_enabled
    _tts_enabled = not _tts_enabled
    return _voice_enabled


def process_turn(user_input, auto_loop, speak_fn=None):
    """Process one user turn and optionally speak the reply."""
    global _tts_enabled

    speak_reply = speak_fn or speak
    if not user_input.strip():
        return False

    cmd = user_input.strip().lower()

    # ---- SYSTEM COMMANDS ----
    cmd_tokens = set(cmd.split())
    if cmd == "exit" or cmd == "stop voice chat" or cmd == "quit voice chat" or "exit" in cmd_tokens:
        farewell = "Goodbye. I am glad you are satisfied with my care."
        diya_print(farewell)
        if _tts_enabled:
            if not speak_reply(farewell):
                safe_print("  [TTS warning] Failed to speak farewell.")
                safe_print(f"  {get_tts_diagnostics()}")
        auto_loop.stop()
        return True

    if cmd == "voice":
        state = toggle_voice()
        msg = f"Voice mode {'enabled' if state else 'disabled'}."
        diya_print(msg)
        if state:
            diya_print(get_voice_status())
        return False

    if cmd == "voice status":
        diya_print(get_voice_status())
        return False

    if cmd == "voice debug":
        diya_print(get_voice_status())
        safe_print(f"  {get_tts_diagnostics()}")
        return False

    if cmd in ["help", "brain help", "second brain help"]:
        try:
            with open("SECOND_BRAIN_GUIDE.md", "r", encoding="utf-8") as f:
                guide = f.read()
            safe_print("\n" + guide)
        except FileNotFoundError:
            diya_print("Second brain guide not found.")
        return False

    if cmd == "commands":
        commands_list = """
Available Commands:

VOICE:
  'voice'          - Toggle voice on/off
  'voice status'   - Show voice system status
  'voice debug'    - Show detailed TTS diagnostics

HELP & INFO:
  'help'           - Show second brain guide
  'commands'       - Show this list
  'status'         - Show current state
  'modes'          - List personality modes
  'my tasks'       - Show to-do list

PERSONALITY:
  'friend mode'    - Switch to friend mode
  'engineer mode'  - Switch to engineer mode
  'roast mode'     - Switch to roast mode
  'deep mode'      - Switch to deep mode
  'emotional mode' - Switch to emotional mode
  'assistant mode' - Switch to assistant mode

SESSION:
  '--voice-chat'   - Run voice-to-voice chat
  '--autonomous'   - Run unattended
  'exit'           - Stop Diya

Try talking naturally! Diya handles:
  - Tasks (add/list/schedule)
  - Notes (capture/search)
  - Habits (track/check)
  - Projects (manage/progress)
  - Insights (daily/weekly)
  - Questions (web search)
  - Code help (debugging)
"""
        safe_print(commands_list)
        return False

    if cmd == "wake up" and get_current_state() == "sleeping":
        wake_up_manually(30) # Stay awake for 30 mins
        auto_loop.set_wake_announced(True)
        msg = "*groggily* Mmm... you woke me up... okay, I am here."
        diya_print(msg)
        if _tts_enabled:
            speak_reply(msg)
        auto_loop.notify_user_interaction()
        return False

    # ---- PROCESS THROUGH BRAIN ----
    auto_loop.pause()
    auto_loop.notify_user_interaction()

    reply = think(user_input)

    # Add state flavor
    state = get_current_state()
    if state == "sleepy" and not reply.startswith("*"):
        reply = f"*yawns* {reply}"
    elif state == "waking_up" and not reply.startswith("*"):
        reply = f"*still waking up* {reply}"

    timestamp = datetime.now().strftime("%H:%M")
    safe_print(f"[{timestamp}] Diya: {reply}")

    if _tts_enabled:
        if not speak_reply(reply):
            safe_print("  [TTS warning] Reply voice output failed.")
            safe_print(f"  {get_tts_diagnostics()}")

    # Update life cycle memory
    memory = load_memory()
    memory["life_cycle"]["last_user_interaction"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_memory(memory)

    auto_loop.resume()
    return False


def run_voice_chat_session(auto_loop):
    """Run a continuous voice-to-voice conversation loop with simultaneous interaction."""
    if not is_stt_available():
        safe_print("  Voice chat is unavailable. Install SpeechRecognition and PyAudio, then try again.")
        return

    safe_print("  ============================================================")
    safe_print("   SIMULTANEOUS VOICE CHAT ACTIVE")
    safe_print("   Speak naturally; Diya will listen even while she speaks.")
    safe_print("   Say 'exit' or 'stop voice chat' to stop.")
    safe_print("  ============================================================")

    input_queue = queue.Queue()

    def stt_callback(text):
        if text:
            # Barge-in: Stop speaking immediately when user speaks
            stop_speaking()
            input_queue.put(text)

    # Start continuous background listener
    stop_listening = listen_continuous(stt_callback)

    try:
        while True:
            try:
                # Wait for user input from the queue
                user_input = input_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            if detect_wake_word(user_input):
                stripped = strip_wake_word(user_input)
                if stripped:
                    user_input = stripped

            safe_print(f"You (voice): {user_input}")

            try:
                # Use non-blocking speak by default for fluidity
                finished = process_turn(user_input, auto_loop, speak_fn=speak)
            except Exception as exc:
                safe_print(f"  Voice turn failed: {exc}")
                continue

            if finished:
                break
    finally:
        # Stop background listener when exiting
        stop_listening()
        auto_loop.stop()


# ================= MAIN =================

def main():
    global _voice_enabled, _tts_enabled

    # Check for --voice flag
    if "--voice" in sys.argv:
        _voice_enabled = True
        _tts_enabled = True

    autonomous_mode = "--autonomous" in sys.argv or "--daemon" in sys.argv
    voice_chat_mode = "--voice-chat" in sys.argv or "--talk" in sys.argv
    if voice_chat_mode:
        _voice_enabled = True
        _tts_enabled = True

    # Load memory
    memory = load_memory()
    current_state = get_current_state()
    props = get_state_properties(current_state)
    mode = memory.get("personality_mode", {}).get("current", "friend")
    mode_info = get_mode_info(mode)

    # -------- STARTUP BANNER --------
    safe_print("")
    safe_print("=" * 60)
    safe_print("     DIYA - Autonomous AI Healthcare Companion")
    safe_print("     She lives, thinks, and speaks on her own.")
    safe_print("=" * 60)
    safe_print(f"  State: {current_state:<12} | Mood: {props['mood']}")
    safe_print(f"  Energy: {props['energy'] * 100:.0f}%{'':<10} | Mode: {mode_info['emoji']} {mode_info['name']}")
    safe_print(f"  TTS: {'ON' if _tts_enabled else 'OFF':<14} | STT: {'ON' if _voice_enabled else 'OFF'}")
    safe_print("=" * 60)
    safe_print("")
    safe_print("  Commands:")
    safe_print("    'modes'         - List personality modes")
    safe_print("    'friend mode'   - Switch to Friend mode")
    safe_print("    'engineer mode' - Switch to Engineer mode")
    safe_print("    'roast mode'    - Switch to Roast mode")
    safe_print("    'voice'         - Toggle voice on/off")
    safe_print("    '--voice-chat'  - Run continuous voice-to-voice chat")
    safe_print("    '--autonomous'   - Run unattended with self-directed background activity")
    safe_print("    'status'        - Show current context")
    safe_print("    'my tasks'      - Show to-do list")
    safe_print("    'exit'          - Stop Diya")
    safe_print("")

    # -------- STATE-AWARE GREETING --------
    if current_state == "sleeping":
        greeting = "*zzz*... *mumbles*... I am sleeping... type 'wake up' to rouse me..."
    elif memory["state"]["awaiting_preferred_name"]:
        greeting = "Hello. I am Diya, your personal AI companion. What should I call you?"
    else:
        name = memory["identity"].get("preferred_name", "friend")
        if current_state == "waking_up":
            greeting = get_wakeup_message(memory)
        elif current_state == "sleepy":
            greeting = f"*yawns* Oh, {name}... I am quite sleepy but I am here for you."
        elif current_state == "evening":
            greeting = f"Good evening, {name}. The day is winding down. How are you?"
        elif current_state == "morning":
            greeting = f"Good morning, {name}! I feel calm and ready for the day."
        elif current_state == "active":
            greeting = f"Hey {name}! I'm feeling energetic and ready to go!"
        else:
            greeting = f"Hello, {name}! I am Diya. Feeling {props['mood']} right now."

    diya_print(greeting)
    if _tts_enabled:
        if _voice_enabled:
            if not speak_blocking(greeting):
                safe_print("  [TTS warning] Startup greeting was not spoken.")
                safe_print(f"  {get_tts_diagnostics()}")
        else:
            if not speak(greeting):
                safe_print("  [TTS warning] Startup greeting was not spoken.")
                safe_print(f"  {get_tts_diagnostics()}")

    # -------- START AUTONOMOUS LOOP --------
    auto_loop = DiyaAutonomousLoop(print_fn=diya_print)
    auto_loop.start()

    if voice_chat_mode:
        if not _tts_enabled:
            _tts_enabled = True
        run_voice_chat_session(auto_loop)
        return

    if autonomous_mode:
        safe_print("  Autonomous mode enabled. Diya will keep working without user input.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            farewell = "I will pause autonomous mode now."
            diya_print(farewell)
            if _tts_enabled:
                if not speak(farewell):
                    safe_print("  [TTS warning] Autonomous farewell was not spoken.")
                    safe_print(f"  {get_tts_diagnostics()}")
            auto_loop.stop()
            return

    # -------- MAIN INPUT LOOP --------
    while True:
        try:
            # Voice input mode
            if _voice_enabled and is_stt_available():
                safe_print("\n  [Listening... speak now]")
                user_input = listen(timeout=5, phrase_limit=15)
                if user_input:
                    safe_print(f"You (voice): {user_input}")
                else:
                    continue
            else:
                user_input = input("\nYou: ")
        except (KeyboardInterrupt, EOFError):
            farewell = "I will be here if you need me. Goodbye."
            diya_print(farewell)
            if _tts_enabled:
                if _voice_enabled:
                    if not speak_blocking(farewell):
                        safe_print("  [TTS warning] Exit farewell was not spoken.")
                        safe_print(f"  {get_tts_diagnostics()}")
                else:
                    if not speak(farewell):
                        safe_print("  [TTS warning] Exit farewell was not spoken.")
                        safe_print(f"  {get_tts_diagnostics()}")
            auto_loop.stop()
            break

        speak_fn = speak_blocking if _voice_enabled else speak
        if process_turn(user_input, auto_loop, speak_fn=speak_fn):
            break


if __name__ == "__main__":
    main()
