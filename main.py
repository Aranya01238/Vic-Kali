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
import atexit
import threading
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

_brain_avatar_label = ""
_brain_avatar_window = None
_brain_avatar_controller = None


def _set_brain_avatar_label(memory):
    """Cache the brain's avatar identity for speech output."""
    global _brain_avatar_label
    avatar_path = memory.get("identity", {}).get("avatar_path", "")
    _brain_avatar_label = f"[brain face: {avatar_path}]" if avatar_path else ""


def _set_brain_avatar_controller(controller):
    """Cache the active avatar controller for lip-sync/blink cues."""
    global _brain_avatar_controller
    _brain_avatar_controller = controller


def _avatar_supports_motion():
    return _brain_avatar_controller is not None and hasattr(_brain_avatar_controller, "set_lipsync")


def _avatar_mouth_level(message):
    words = max(1, len((message or "").split()))
    level = 0.18 + min(0.82, words / 18.0)
    return max(0.12, min(1.0, level))


def _avatar_set_mouth(level):
    if not _avatar_supports_motion():
        return
    try:
        _brain_avatar_controller.set_lipsync(max(0.0, min(1.0, float(level))))
    except Exception:
        pass


def _avatar_blink():
    if not _avatar_supports_motion():
        return
    try:
        _brain_avatar_controller.blink()
    except Exception:
        pass


def speak_with_avatar(message, speak_fn, blocking=False):
    """Speak and drive avatar mouth motion while the message is spoken."""
    import threading as _threading

    if _avatar_supports_motion():
        _avatar_set_mouth(_avatar_mouth_level(message))

    ok = speak_fn(message)

    if _avatar_supports_motion():
        duration = max(0.8, min(4.0, len(message or "") / 12.0))
        if blocking:
            _avatar_set_mouth(0.0)
            _avatar_blink()
        else:
            def _reset():
                _avatar_set_mouth(0.0)
                _avatar_blink()

            _threading.Timer(duration, _reset).start()

    return ok


class BrainAvatarWindow:
    """Tiny always-on-top avatar window for Diya."""

    def __init__(self, avatar_path, title="Diya"):
        self.avatar_path = avatar_path
        self.title = title
        self._thread = None
        self._root = None
        self._stop_requested = threading.Event()
        self._ready = threading.Event()

    def _scale_photo(self, image, max_size=220):
        """Shrink a Tk photo image to fit within a square viewport."""
        width = max(1, int(image.width()))
        height = max(1, int(image.height()))
        scale = max(1, (max(width, height) + max_size - 1) // max_size)
        if scale <= 1:
            return image
        return image.subsample(scale, scale)

    def start(self):
        if self._thread:
            return self

        self._thread = threading.Thread(target=self._run, daemon=True, name="BrainAvatarWindow")
        self._thread.start()
        self._ready.wait(timeout=3)
        return self

    def _run(self):
        try:
            import tkinter as tk
        except Exception:
            self._ready.set()
            return

        try:
            root = tk.Tk()
            self._root = root
            root.title(self.title)
            root.configure(bg="#0f0f12")
            root.geometry("320x380+40+40")
            root.resizable(False, False)
            try:
                root.attributes("-topmost", True)
            except Exception:
                pass

            canvas = tk.Canvas(
                root,
                width=280,
                height=300,
                bg="#0f0f12",
                highlightthickness=0,
                bd=0,
            )
            canvas.pack(padx=16, pady=16)

            # Build a layered, pseudo-3D avatar using canvas primitives so we can
            # animate breathing, head-tilt and blinking without extra deps.
            face_center = (140, 140)
            face_radius = 105

            # Create layered concentric ovals for soft shading
            layers = []
            for i, color in enumerate(["#1b1c21", "#2a2b32", "#3b3c44"]):
                r = face_radius + (6 - i * 3)
                layers.append(canvas.create_oval(
                    face_center[0]-r, face_center[1]-r,
                    face_center[0]+r, face_center[1]+r,
                    fill=color, outline="", tags=("layer",)
                ))

            # Face core (lit)
            face_core = canvas.create_oval(
                face_center[0]-face_radius+12, face_center[1]-face_radius+12,
                face_center[0]+face_radius-12, face_center[1]+face_radius-12,
                fill="#fbfbfb", outline="", tags=("face_core",)
            )

            # Inner highlight (gives round volumetric look)
            highlight = canvas.create_oval(
                face_center[0]-face_radius+34, face_center[1]-face_radius+20,
                face_center[0]+face_radius-34, face_center[1]+face_radius-28,
                fill="#ffffff", outline="", stipple="gray12", tags=("highlight",)
            )

            # Eye placeholders (we animate positions / blink)
            eye_radius = 8
            left_eye = canvas.create_oval(0,0,0,0, fill="#0d0d0d", outline="")
            right_eye = canvas.create_oval(0,0,0,0, fill="#0d0d0d", outline="")
            connector = canvas.create_line(0,0,0,0, fill="#0d0d0d", width=6, capstyle=tk.ROUND)

            # Status text and indicators
            canvas.create_text(140, 286, text="Baymax face = brain face", fill="#d7dae3", font=("Segoe UI", 10))
            canvas.create_oval(114, 268, 166, 292, fill="#0f0f12", outline="")
            canvas.create_oval(123, 277, 132, 286, fill="#79ffb3", outline="")
            canvas.create_text(165, 280, text="live", fill="#9da6b7", font=("Segoe UI", 8))

            # Animation state
            import math
            start_t = time.time()
            blink_state = {"closing": False, "pct": 0.0, "last_blink": start_t}

            def _update_avatar():
                t = time.time() - start_t
                # breathing: slow scale factor
                breath = 1.0 + 0.02 * math.sin(t * 1.5)
                # head tilt: small x offset
                tilt = 6 * math.sin(t * 0.6)

                # compute current face bbox
                r = int(face_radius * breath)
                cx = face_center[0] + int(tilt)
                cy = face_center[1]

                # update layered shading positions
                for idx, item in enumerate(layers):
                    offset = idx * 3
                    rr = r + (6 - idx * 3)
                    canvas.coords(item, cx-rr, cy-rr, cx+rr, cy+rr)

                canvas.coords(face_core, cx-r+12, cy-r+12, cx+r-12, cy+r-12)
                canvas.coords(highlight, cx-r+34, cy-r+20, cx+r-34, cy+r-28)

                # eyes move subtly with tilt and breathing
                eye_dx = int(18 * breath + tilt * 0.6)
                eye_dy = int(-6 * (breath - 1))
                left_cx = cx - eye_dx
                right_cx = cx + eye_dx
                eye_cy = cy + eye_dy

                # blinking: trigger every ~3-6s
                now = time.time()
                if now - blink_state["last_blink"] > 3.0 + (math.sin(t) + 1) * 1.5:
                    blink_state["last_blink"] = now
                    blink_state["closing"] = True

                # animate blink percentage
                if blink_state["closing"]:
                    blink_state["pct"] += 0.18
                    if blink_state["pct"] >= 1.0:
                        blink_state["pct"] = 1.0
                        blink_state["closing"] = False
                else:
                    if blink_state["pct"] > 0:
                        blink_state["pct"] -= 0.12
                        if blink_state["pct"] < 0:
                            blink_state["pct"] = 0

                blink = blink_state["pct"]

                # eye geometry depends on blink
                def eye_coords(cx_e, cy_e, r_e, closed_pct):
                    if closed_pct <= 0:
                        return (cx_e-r_e, cy_e-r_e, cx_e+r_e, cy_e+r_e)
                    # when closed, shrink height
                    h = max(1, int(r_e * (1 - closed_pct * 0.98)))
                    return (cx_e-r_e, cy_e-h, cx_e+r_e, cy_e+h)

                canvas.coords(left_eye, *eye_coords(left_cx, eye_cy, eye_radius, blink))
                canvas.coords(right_eye, *eye_coords(right_cx, eye_cy, eye_radius, blink))
                canvas.coords(connector, left_cx+6, eye_cy, right_cx-6, eye_cy)

                # subtle connector width变化 (thicken slightly on inhale)
                canvas.itemconfig(connector, width=max(4, int(6 * (1 + 0.2 * (breath-1)))))

                if not self._stop_requested.is_set():
                    root.after(50, _update_avatar)

            # kick off animation loop
            root.after(100, _update_avatar)

            root.protocol("WM_DELETE_WINDOW", self.stop)
            self._ready.set()

            def _poll_stop():
                if self._stop_requested.is_set():
                    try:
                        root.destroy()
                    except Exception:
                        pass
                    return
                root.after(150, _poll_stop)

            root.after(150, _poll_stop)
            root.mainloop()
        except Exception:
            self._ready.set()
            return

    def stop(self):
        self._stop_requested.set()
        root = self._root
        if root is not None:
            try:
                root.after(0, root.destroy)
            except Exception:
                try:
                    root.destroy()
                except Exception:
                    pass

def safe_print(message):
    """Print safely on Windows terminals."""
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode("ascii", "replace").decode())


def diya_print(message):
    """Print a message from Diya with timestamp."""
    timestamp = datetime.now().strftime("%H:%M")
    face = f" {_brain_avatar_label}" if _brain_avatar_label else ""
    safe_print(f"\n[{timestamp}] Diya{face}: {message}")


def _start_brain_avatar_window(memory):
    """Start the brain avatar window when TTS/voice mode is active."""
    global _brain_avatar_window

    avatar_path = memory.get("identity", {}).get("avatar_path", "")
    if not avatar_path:
        return None

    # Prefer GPU 3D avatar if available (runs as subprocess). Fall back to Tkinter.
    try:
        from avatar_client import Avatar3D

        av = Avatar3D()
        av.start()
        if not getattr(av, "connected", False):
            raise RuntimeError("3D avatar did not report a connected display")
        _brain_avatar_window = av
        _set_brain_avatar_controller(av)
        atexit.register(av.stop)
        return av
    except Exception:
        # Fall back to lightweight Tkinter avatar
        window = BrainAvatarWindow(avatar_path).start()
        _brain_avatar_window = window
        _set_brain_avatar_controller(None)
        atexit.register(window.stop)
        return window


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
    _set_brain_avatar_label(memory)
    avatar_window = _start_brain_avatar_window(memory) if _tts_enabled else None
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
    if _brain_avatar_label:
        safe_print(f"  Face: {_brain_avatar_label}")
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
            if not speak_with_avatar(greeting, speak_blocking, blocking=True):
                safe_print("  [TTS warning] Startup greeting was not spoken.")
                safe_print(f"  {get_tts_diagnostics()}")
        else:
            if not speak_with_avatar(greeting, speak, blocking=False):
                safe_print("  [TTS warning] Startup greeting was not spoken.")
                safe_print(f"  {get_tts_diagnostics()}")

    # -------- START AUTONOMOUS LOOP --------
    auto_loop = DiyaAutonomousLoop(print_fn=diya_print)
    auto_loop.start()

    if voice_chat_mode:
        if not _tts_enabled:
            _tts_enabled = True
        run_voice_chat_session(auto_loop)
        if avatar_window:
            avatar_window.stop()
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
                if not speak_with_avatar(farewell, speak, blocking=False):
                    safe_print("  [TTS warning] Autonomous farewell was not spoken.")
                    safe_print(f"  {get_tts_diagnostics()}")
            auto_loop.stop()
            if avatar_window:
                avatar_window.stop()
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
                    if not speak_with_avatar(farewell, speak_blocking, blocking=True):
                        safe_print("  [TTS warning] Exit farewell was not spoken.")
                        safe_print(f"  {get_tts_diagnostics()}")
                else:
                    if not speak_with_avatar(farewell, speak, blocking=False):
                        safe_print("  [TTS warning] Exit farewell was not spoken.")
                        safe_print(f"  {get_tts_diagnostics()}")
            auto_loop.stop()
            if avatar_window:
                avatar_window.stop()
            break

        speak_fn = (lambda msg: speak_with_avatar(msg, speak_blocking, blocking=True)) if _voice_enabled else (lambda msg: speak_with_avatar(msg, speak, blocking=False))
        if process_turn(user_input, auto_loop, speak_fn=speak_fn):
            if avatar_window:
                avatar_window.stop()
            break


if __name__ == "__main__":
    main()
