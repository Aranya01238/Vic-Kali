"""
voice_system.py - Diya's Voice Interaction System

Speech-to-text (input), text-to-speech (output), and wake word detection.
Uses pyttsx3 for TTS and speech_recognition for STT.
Falls back gracefully if libraries are not installed.
"""

import threading
import platform

# ================= TTS (Text-to-Speech) =================

_tts_engine = None
_tts_available = False
_tts_lock = threading.Lock()
_tts_last_error = ""
_tts_backend = "none"
_sapi_voice = None


def _init_sapi_tts():
    """Initialize native Windows SAPI voice backend."""
    global _sapi_voice
    if platform.system().lower() != "windows":
        return False

    try:
        import win32com.client
        _sapi_voice = win32com.client.Dispatch("SAPI.SpVoice")
        return True
    except Exception:
        _sapi_voice = None
        return False


def _init_tts():
    """Initialize text-to-speech engine."""
    global _tts_engine, _tts_available, _tts_last_error, _tts_backend

    # Prefer native SAPI on Windows for better runtime stability.
    if _init_sapi_tts():
        _tts_available = True
        _tts_backend = "sapi"
        _tts_last_error = ""
        return True

    try:
        import pyttsx3
        _tts_engine = pyttsx3.init()
        # Set properties
        _tts_engine.setProperty("rate", 160)  # Speed
        _tts_engine.setProperty("volume", 0.9)

        # Try to use a female voice
        voices = _tts_engine.getProperty("voices")
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                _tts_engine.setProperty("voice", voice.id)
                break

        _tts_available = True
        _tts_backend = "pyttsx3"
        _tts_last_error = ""
        return True
    except Exception as exc:
        _tts_last_error = str(exc)
        _tts_available = False
        _tts_engine = None
        _tts_backend = "none"
        return False


def _speak_with_sapi(clean_text, async_mode=False):
    """Speak using native Windows SAPI backend."""
    global _tts_last_error
    if not _sapi_voice:
        _tts_last_error = "SAPI backend not initialized"
        return False

    try:
        if clean_text:
            # Flags: 1 = SVSFlagsAsync
            flags = 1 if async_mode else 0
            _sapi_voice.Speak(clean_text, flags)
        _tts_last_error = ""
        return True
    except Exception as exc:
        _tts_last_error = str(exc)
        return False


def stop_speaking():
    """Stop any current speech immediately."""
    global _tts_backend, _sapi_voice, _tts_engine
    if _tts_backend == "sapi" and _sapi_voice:
        try:
            # Flags: 1 = Async, 2 = PurgeBeforeSpeak
            _sapi_voice.Speak("", 1 | 2)
        except Exception:
            pass
    elif _tts_backend == "pyttsx3" and _tts_engine:
        try:
            _tts_engine.stop()
        except Exception:
            pass


def _speak_once(clean_text, async_mode=False):
    """Speak one chunk of text once using the current engine."""
    global _tts_last_error

    if _tts_backend == "sapi":
        return _speak_with_sapi(clean_text, async_mode=async_mode)

    try:
        if clean_text:
            _tts_engine.say(clean_text)
            _tts_engine.runAndWait()
        _tts_last_error = ""
        return True
    except Exception as exc:
        _tts_last_error = str(exc)
        return False


def speak(text, async_mode=True):
    """Speak text aloud using TTS. Defaults to non-blocking."""
    global _tts_engine, _tts_available

    if not _tts_available:
        if not _init_tts():
            return False

    clean = text.encode("ascii", "ignore").decode().strip()
    
    if _tts_backend == "sapi" and async_mode:
        return _speak_with_sapi(clean, async_mode=True)

    def _speak_thread():
        # Reuse blocking path for reliability + retry behavior.
        speak_blocking(clean)

    t = threading.Thread(target=_speak_thread, daemon=True)
    t.start()
    return True


def speak_blocking(text):
    """Speak text aloud using TTS and wait until the speech is finished."""
    global _tts_engine, _tts_available, _tts_last_error

    if not _tts_available:
        if not _init_tts():
            return False

    with _tts_lock:
        clean = text.encode("ascii", "ignore").decode().strip()
        if _speak_once(clean, async_mode=False):
            return True

        # One retry with a fresh engine for transient pyttsx3 failures.
        _tts_available = False
        _tts_engine = None
        if not _init_tts():
            return False
        if not _speak_once(clean, async_mode=False):
            return False

    return True


def is_tts_available():
    """Check if TTS is available."""
    global _tts_available
    if not _tts_available:
        _init_tts()
    return _tts_available


# ================= STT (Speech-to-Text) =================

_stt_available = False


def _check_stt():
    """Check if speech recognition is available."""
    global _stt_available
    try:
        import speech_recognition
        _stt_available = True
    except ImportError:
        _stt_available = False
    return _stt_available


def listen(timeout=5, phrase_limit=10):
    """Listen to microphone and return recognized text (blocking)."""
    if not _check_stt():
        return None

    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True

        mic = sr.Microphone()
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("  [Listening...]")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)

        text = recognizer.recognize_google(audio)
        return text

    except Exception:
        return None


def listen_continuous(callback):
    """
    Start continuous listening in the background.
    Calls 'callback(text)' whenever speech is recognized.
    Returns a function that can be called to stop the background listener.
    """
    if not _check_stt():
        return lambda: None

    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True
        
        # Lower ambient noise adjustment time for responsiveness
        mic = sr.Microphone()
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

        def _internal_callback(recognizer, audio):
            try:
                text = recognizer.recognize_google(audio)
                if text:
                    callback(text)
            except Exception:
                pass

        # Returns a function to stop the listener
        stop_fn = recognizer.listen_in_background(mic, _internal_callback)
        return stop_fn

    except Exception as e:
        print(f"  [STT error] Could not start continuous listener: {e}")
        return lambda: None


def is_stt_available():
    """Check if STT is available."""
    return _check_stt()


# ================= WAKE WORD DETECTION =================

WAKE_WORDS = ["hey diya", "diya", "hey aira", "aira", "wake up"]


def detect_wake_word(text):
    """Check if the text contains a wake word."""
    if not text:
        return False
    t = text.lower().strip()
    return any(t.startswith(w) or t == w for w in WAKE_WORDS)


def strip_wake_word(text):
    """Remove the wake word from the beginning of text."""
    if not text:
        return text
    t = text.lower().strip()
    for w in WAKE_WORDS:
        if t.startswith(w):
            result = text[len(w):].strip()
            # Remove leading punctuation
            result = result.lstrip(",!. ")
            return result if result else text
    return text


# ================= VOICE LOOP =================

def voice_input_loop(callback, stop_event=None):
    """
    Continuous voice input loop. Calls callback(text) for each recognized phrase.
    Runs until stop_event is set.
    """
    if not is_stt_available():
        print("  Voice input not available. Install: pip install SpeechRecognition pyaudio")
        return

    print("  Voice mode active. Say 'Hey Diya' to start, or just speak.")

    while stop_event is None or not stop_event.is_set():
        text = listen(timeout=3, phrase_limit=15)
        if text:
            # Check for wake word or just pass through
            if detect_wake_word(text):
                clean_text = strip_wake_word(text)
                if clean_text:
                    callback(clean_text)
            else:
                # Still process even without wake word
                callback(text)


# ================= STATUS =================

def get_voice_status():
    """Get status of voice systems."""
    tts = "Available" if is_tts_available() else "Not installed (pip install pyttsx3)"
    stt = "Available" if is_stt_available() else "Not installed (pip install SpeechRecognition pyaudio)"
    backend = _tts_backend if _tts_backend != "none" else "uninitialized"
    return f"Voice System Status:\n  TTS (Text-to-Speech): {tts}\n  STT (Speech-to-Text): {stt}\n  TTS Backend: {backend}"


def get_tts_diagnostics():
    """Get compact diagnostics for TTS runtime failures."""
    status = "ready" if is_tts_available() else "unavailable"
    err = _tts_last_error.strip()
    backend = _tts_backend if _tts_backend != "none" else "uninitialized"
    if err:
        return f"TTS status: {status} | backend: {backend} | last error: {err}"
    return f"TTS status: {status} | backend: {backend} | last error: none"
