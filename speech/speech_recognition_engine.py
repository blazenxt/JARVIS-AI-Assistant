"""
======================================================
JARVIS AI ASSISTANT - SPEECH RECOGNITION ENGINE
======================================================
Captures voice commands from the microphone and converts
them to text. Supports text-input fallback if no mic is found.
"""

import sys
import time
from typing import Optional, Callable
import config

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False


class SpeechInputEngine:
    """
    JARVIS Hearing Engine: Captures voice commands via Microphone
    or keyboard fallback.
    """

    def __init__(self, language: str = "en-IN"):
        self.language = language
        self.recognizer = sr.Recognizer() if SR_AVAILABLE else None
        self.mic = None
        self.mic_available = False
        self.on_listen_status: Optional[Callable[[str], None]] = None

        self._check_mic_availability()

    def _check_mic_availability(self):
        """Check if a working microphone is connected."""
        if not SR_AVAILABLE:
            self.mic_available = False
            return

        try:
            mic_list = sr.Microphone.list_microphone_names()
            if len(mic_list) > 0:
                self.mic_available = True
            else:
                self.mic_available = False
        except Exception:
            self.mic_available = False

    def listen(self, prompt: str = "Listening...", timeout: int = 5, phrase_time_limit: int = 8, force_text_mode: bool = False) -> str:
        """
        Listen for a voice command.
        If force_text_mode is True or microphone is unavailable, use keyboard input.
        """
        if force_text_mode or not self.mic_available:
            return self._listen_text_mode()

        try:
            if self.on_listen_status:
                self.on_listen_status("LISTENING")

            print(f"\n[JARVIS Ear]: {prompt}", end="", flush=True)

            with sr.Microphone() as source:
                # Adjust for ambient noise briefly
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

            if self.on_listen_status:
                self.on_listen_status("PROCESSING")

            print(" Processing...")
            # Recognize speech using Google Speech API (free default in speech_recognition)
            query = self.recognizer.recognize_google(audio, language=self.language)
            print(f"[You]: {query}")
            return query.strip()

        except sr.WaitTimeoutError:
            print(" (No speech detected)")
            return ""
        except sr.UnknownValueError:
            print(" (Could not understand audio)")
            return ""
        except sr.RequestError as e:
            print(f" [Speech API Error: {e} -> Switching to text fallback]")
            return self._listen_text_mode()
        except Exception as e:
            print(f" [Microphone Error: {e} -> Switching to text fallback]")
            self.mic_available = False
            return self._listen_text_mode()
        finally:
            if self.on_listen_status:
                self.on_listen_status("STANDBY")

    def _listen_text_mode(self) -> str:
        """Fallback input method using keyboard CLI."""
        try:
            user_input = input("\n[You (Type command)]: ").strip()
            return user_input
        except (KeyboardInterrupt, EOFError):
            print("\n[JARVIS]: Shutting down systems...")
            sys.exit(0)

    def wait_for_wake_word(self, wake_word: str = config.WAKE_WORD) -> bool:
        """
        Continuously listen for the wake word (e.g., 'Jarvis').
        Returns True once detected.
        """
        if not self.mic_available:
            # In text mode, we don't block on wake word; user types commands directly
            return True

        print(f"\n[JARVIS Standby]: Say '{wake_word}' to activate...")
        while True:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.6)
                    audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=4)
                text = self.recognizer.recognize_google(audio, language=self.language).lower()
                if wake_word.lower() in text:
                    print(f"[Wake Word Detected]: '{text}'")
                    return True
            except (sr.UnknownValueError, sr.WaitTimeoutError):
                continue
            except Exception as e:
                print(f"[Wake Word Error] {e}. Switching to direct command mode.")
                return True


# Global singleton
_speech_singleton = None

def get_speech_engine(language: str = "en-IN") -> SpeechInputEngine:
    global _speech_singleton
    if _speech_singleton is None:
        _speech_singleton = SpeechInputEngine(language=language)
    return _speech_singleton
