"""
======================================================
JARVIS AI ASSISTANT - TEXT TO SPEECH (TTS) ENGINE
======================================================
Provides natural neural voice output using Microsoft Edge TTS
with offline fallback support via pyttsx3.
"""

import os
import time
import platform
import asyncio
import threading
from pathlib import Path
from typing import Optional, Callable
import config

# Try importing edge_tts
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# Try importing pygame for MP3 playback (Only on local systems with audio hardware)
PYGAME_AVAILABLE = False
try:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
    import pygame
    # Only initialize pygame mixer if we are not on a headless Linux server without audio
    if platform.system() in ["Windows", "Darwin"] or os.environ.get("DISPLAY"):
        pygame.mixer.init()
        PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False

# Try importing pyttsx3 for offline TTS fallback
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False


class TTSEngine:
    """
    JARVIS Voice Engine: Handles speaking text aloud with sci-fi natural tone.
    Supports callbacks for UI status updates (e.g. updating Web HUD to 'SPEAKING').
    """

    def __init__(self, engine_type: str = config.TTS_ENGINE, voice: str = config.EDGE_TTS_VOICE):
        self.engine_type = engine_type.lower()
        self.voice = voice
        self.is_speaking = False
        self.on_speak_start: Optional[Callable[[str], None]] = None
        self.on_speak_end: Optional[Callable[[], None]] = None

        # Initialize offline pyttsx3 engine if needed
        self.offline_engine = None
        if PYTTSX3_AVAILABLE:
            try:
                self.offline_engine = pyttsx3.init()
                self.offline_engine.setProperty('rate', 185)  # Crisp speaking rate
            except Exception as e:
                print(f"[TTS Warning] Could not initialize pyttsx3: {e}")

    def speak(self, text: str, print_to_console: bool = True):
        """
        Speak the provided text string aloud.
        Automatically falls back to offline TTS or console output if needed.
        """
        if not text or not text.strip():
            return

        clean_text = text.strip()
        if print_to_console:
            print(f"\n[{config.JARVIS_NAME}]: {clean_text}")

        self.is_speaking = True
        if self.on_speak_start:
            try:
                self.on_speak_start(clean_text)
            except Exception:
                pass

        try:
            # 1. Try Edge-TTS (Best quality neural AI voice)
            if self.engine_type == "edge-tts" and EDGE_TTS_AVAILABLE and PYGAME_AVAILABLE:
                success = self._speak_edge_tts(clean_text)
                if not success:
                    self._speak_offline_pyttsx3(clean_text)
            else:
                # 2. Try offline pyttsx3
                self._speak_offline_pyttsx3(clean_text)
        except Exception as e:
            print(f"[TTS Error] Voice output failed ({e}). Text displayed above.")
        finally:
            self.is_speaking = False
            if self.on_speak_end:
                try:
                    self.on_speak_end()
                except Exception:
                    pass

    def _speak_edge_tts(self, text: str) -> bool:
        """Synthesize and play audio using Edge TTS neural voices."""
        try:
            audio_file = config.AUDIO_CACHE_DIR / "speech_output.mp3"
            if audio_file.exists():
                try:
                    audio_file.unlink()
                except Exception:
                    pass

            # Run async edge_tts in a new event loop
            async def generate_speech():
                communicate = edge_tts.Communicate(
                    text=text,
                    voice=self.voice,
                    rate=config.TTS_RATE,
                    volume=config.TTS_VOLUME
                )
                await communicate.save(str(audio_file))

            try:
                asyncio.run(generate_speech())
            except RuntimeError:
                # If an event loop is already running
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(generate_speech())
                loop.close()

            if audio_file.exists():
                return self._play_mp3_pygame(audio_file)
            return False
        except Exception as e:
            print(f"[Edge-TTS Warning] Falling back to offline voice: {e}")
            return False

    def _play_mp3_pygame(self, file_path: Path) -> bool:
        """Play MP3 audio using PyGame mixer."""
        try:
            pygame.mixer.music.load(str(file_path))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.music.unload()
            return True
        except Exception as e:
            print(f"[Audio Playback Error] {e}")
            return False

    def _speak_offline_pyttsx3(self, text: str):
        """Fallback to offline pyttsx3 speech synthesizer."""
        if self.offline_engine:
            try:
                self.offline_engine.say(text)
                self.offline_engine.runAndWait()
            except Exception as e:
                print(f"[Offline TTS Error] {e}")


# Global singleton instance for easy imports across skills
_tts_singleton = None

def get_tts_engine() -> TTSEngine:
    global _tts_singleton
    if _tts_singleton is None:
        _tts_singleton = TTSEngine()
    return _tts_singleton

def speak(text: str, print_to_console: bool = True):
    """Convenience helper to speak text using the global JARVIS TTS engine."""
    engine = get_tts_engine()
    engine.speak(text, print_to_console=print_to_console)
