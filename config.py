"""
======================================================
JARVIS AI ASSISTANT - CONFIGURATION MODULE
======================================================
Loads environment variables and sets global defaults for
JARVIS speech, AI LLM backends, skills, and UI server.
"""

import os
from pathlib import Path

# Base Directory of JARVIS project
BASE_DIR = Path(__file__).parent.resolve()

def load_env_file(filepath: Path):
    """Simple parser for .env files without requiring third-party libraries."""
    if not filepath.exists():
        return
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip("'").strip('"')
                if key and not os.getenv(key):
                    os.environ[key] = val
    except Exception as e:
        print(f"[Config Warning] Could not load {filepath}: {e}")

# Load .env if present, otherwise .env.example
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_env_file(env_path)
else:
    load_env_file(BASE_DIR / ".env.example")

# --- AI BRAIN SETTINGS ---
AI_BACKEND = os.getenv("AI_BACKEND", "offline").lower()

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

# Google Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# --- SPEECH SETTINGS ---
TTS_ENGINE = os.getenv("TTS_ENGINE", "edge-tts").lower()
EDGE_TTS_VOICE = os.getenv("EDGE_TTS_VOICE", "en-GB-RyanNeural")
TTS_RATE = os.getenv("TTS_RATE", "+0%")
TTS_VOLUME = os.getenv("TTS_VOLUME", "+0%")
WAKE_WORD = os.getenv("WAKE_WORD", "jarvis").lower()

# --- USER & ENVIRONMENT ---
USER_NAME = os.getenv("USER_NAME", "Sir")
JARVIS_NAME = os.getenv("JARVIS_NAME", "JARVIS")
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Asansol")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# --- STORAGE PATHS ---
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
NOTES_FILE = DATA_DIR / "notes.txt"
TODO_FILE = DATA_DIR / "todo.json"
AUDIO_CACHE_DIR = DATA_DIR / "audio_cache"
AUDIO_CACHE_DIR.mkdir(exist_ok=True)

# --- WEB HUD SERVER SETTINGS ---
WEB_HOST = "0.0.0.0"
WEB_PORT = int(os.getenv("PORT", 8000))

def get_status_summary() -> dict:
    """Return a dictionary summarizing current JARVIS config status."""
    return {
        "jarvis_name": JARVIS_NAME,
        "user_name": USER_NAME,
        "ai_backend": AI_BACKEND,
        "tts_engine": TTS_ENGINE,
        "voice": EDGE_TTS_VOICE,
        "default_city": DEFAULT_CITY,
        "has_groq_key": bool(GROQ_API_KEY and "your_" not in GROQ_API_KEY),
        "has_gemini_key": bool(GEMINI_API_KEY and "your_" not in GEMINI_API_KEY),
        "has_openai_key": bool(OPENAI_API_KEY and "your_" not in OPENAI_API_KEY),
    }
