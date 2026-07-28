# J.A.R.V.I.S. // Just A Rather Very Intelligent System
### Production-Ready Modular AI Voice & System Assistant Suite with Sci-Fi Web HUD

![JARVIS Banner](https://img.shields.io/badge/AI_Assistant-J.A.R.V.I.S.-00f3ff?style=for-the-badge&logo=python&logoColor=white)
![Python Version](https://img.shields.io/badge/Python-3.9%2B-ffbe0b?style=for-the-badge&logo=python)
![Web HUD](https://img.shields.io/badge/Sci--Fi_HUD-Iron_Man_Edition-ff3366?style=for-the-badge)

Welcome to **J.A.R.V.I.S.** — an elite, multi-modal, highly intelligent personal AI assistant inspired by Tony Stark's iconic AI from Iron Man. This suite combines a robust modular Python backend with an interactive glowing Holographic Web HUD dashboard.

---

## 🚀 Key Features

1. **Multi-Modal Voice Input & Speech Output**:
   - **Speech Recognition**: Microphone speech recognition (`speech_recognition` with Google Speech API) with automatic keyboard/CLI fallback if no microphone is found. Supports English, Hindi, and Hinglish (`en-IN`, `hi-IN`, `en-US`).
   - **Neural TTS Voice**: Uses high-quality Microsoft Edge Neural TTS (`edge-tts`) for realistic, crisp sci-fi AI narration (like Jarvis's British accent) with offline fallback (`pyttsx3`).

2. **Intelligent Multi-Backend LLM Brain (`brain/llm_engine.py`)**:
   - **Groq API**: Blazing fast Llama-3 / Mixtral inference (Free tier available).
   - **Google Gemini API**: Native Google Generative AI integration.
   - **OpenAI API**: GPT-4o / GPT-3.5 Turbo support.
   - **Ollama**: Connects to local offline LLM models (`http://localhost:11434/v1`).
   - **Smart Offline Intelligence**: Works out-of-the-box even without API keys! Handles greetings, system diagnostics, time/date, jokes, motivational quotes, and identity queries offline.

3. **Modular Desktop & System Skills (`skills/`)**:
   - ⚡ **System Hardware & Telemetry**: Live CPU utilization %, RAM usage (used/total GB), and Battery status via `psutil`.
   - 🖥️ **Application Launcher**: Open desktop applications across Windows, macOS, and Linux (Chrome, VS Code, Notepad, Calculator, Explorer, Terminal).
   - 📸 **Screen Capture**: Take automated screenshots saved to `data/screenshots/`.
   - 🌐 **Web & Search**: Search Google, play YouTube videos/songs, fetch 2-sentence Wikipedia summaries, and open top websites.
   - 📝 **Productivity Suite**: Record timestamped voice notes (`data/notes.txt`), manage an interactive to-do list (`data/todo.json`), and get formatted date/time reports.
   - 🌤️ **Live Weather & News**: Fetch live weather reports (using OpenWeather API or the free `wttr.in` service without needing an API key!) and top headlines.

4. **Holographic Sci-Fi Web HUD (`web_ui/` & `server.py`)**:
   - Futuristic Iron Man Cyan & Gold Arc Reactor with CSS/SVG animations.
   - Real-time voice visualizer & status indicator (`LISTENING`, `PROCESSING`, `SPEAKING`, `STANDBY`).
   - Live telemetry gauges for CPU and RAM load.
   - Built-in **Web Speech API** for browser-based speech recognition and audio synthesis.
   - Live transcript log and quick-action command buttons.

---

## 📂 Architecture & Folder Structure

```
jarvis/
│
├── config.py                 # Core configuration, environment loading, and default fallbacks
├── jarvis.py                 # Main CLI / Voice Assistant engine and interactive loop
├── server.py                 # Lightweight REST API & Web HUD server (Port 8000)
├── requirements.txt          # Python dependencies
├── .env.example              # Example environment variables (copy to .env)
├── README.md                 # Technical documentation & usage guide
├── SETUP_GUIDE_HINDI.md      # Comprehensive Hindi / Hinglish setup guide
│
├── brain/
│   ├── __init__.py
│   └── llm_engine.py         # Multi-backend AI intelligence & conversation memory
│
├── speech/
│   ├── __init__.py
│   ├── speech_recognition_engine.py # Microphone audio capture & CLI text fallback
│   └── text_to_speech.py     # Microsoft Edge Neural TTS + offline fallback
│
├── skills/
│   ├── __init__.py           # Unified command dispatcher (dispatch_command)
│   ├── system_skills.py      # System stats, app launcher, screenshots, power commands
│   ├── web_skills.py         # Google search, Wikipedia, YouTube, website opening
│   ├── productivity_skills.py # Notes manager, to-do task list, time & date
│   └── weather_skills.py     # Weather (wttr.in/OpenWeather) & news headlines
│
├── web_ui/                   # Sci-Fi Holographic Web Dashboard
│   ├── index.html            # Futuristic HUD layout
│   ├── style.css             # Glowing cyan/gold Arc Reactor & scanlines CSS
│   └── script.js             # Web Speech API & live REST telemetry polling
│
└── data/                     # Persistent storage (auto-created)
    ├── notes.txt             # Saved voice notes
    ├── todo.json             # To-do task list
    ├── audio_cache/          # Temporary TTS audio cache
    └── screenshots/          # Captured screen images
```

---

## 🛠️ Installation & Setup

### Step 1: Clone or Open Project
Open a terminal in the project directory:
```bash
cd /path/to/jarvis
```

### Step 2: Install Python Dependencies
Install the required packages using `pip`:
```bash
pip install -r requirements.txt
```
> **Note for Windows users regarding audio input**:
> If you encounter an error installing `pyaudio`, install it via wheel or pipwin:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### Step 3: Configure Environment Variables
Copy `.env.example` to `.env` and enter your preferred API keys:
```bash
cp .env.example .env
```
Inside `.env`, you can choose your AI backend:
- **`AI_BACKEND=groq`** (Recommended! Free & extremely fast Llama-3 API at [console.groq.com/keys](https://console.groq.com/keys))
- **`AI_BACKEND=gemini`** (Free Google Gemini API key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey))
- **`AI_BACKEND=openai`** (OpenAI API key)
- **`AI_BACKEND=offline`** (Smart local rule-based intelligence without any cloud keys!)

---

## 🖥️ How to Run JARVIS

### 1. Interactive CLI & Text/Voice Mode (Default)
Run JARVIS in standard interactive mode. If a microphone is connected, it will listen to your voice; otherwise, it automatically switches to keyboard input:
```bash
python jarvis.py
```

### 2. Continuous Voice Wake-Word Mode
Run in continuous listening mode where JARVIS waits for you to say the wake word (`"Jarvis"` or `"Hey Jarvis"`):
```bash
python jarvis.py --mode voice
```

### 3. Holographic Sci-Fi Web HUD Mode
Launch the glowing Iron Man holographic dashboard and REST server on `http://localhost:8000`:
```bash
python jarvis.py --mode web
# OR directly:
python server.py
```
Open your browser and navigate to **`http://localhost:8000`** to control JARVIS with clickable commands, browser speech recognition, and live CPU/RAM telemetry!

### 4. Automated Sanity Test Suite
Verify that all core modules, system skills, weather API, and AI intelligence are working correctly:
```bash
python jarvis.py --test
```

---

## 🗣️ Voice Commands & Skills Summary

| Command Phrase | Action / Skill Executed |
| :--- | :--- |
| `"System stats"` / `"CPU usage"` | Reports live CPU load, RAM usage %, and battery status. |
| `"What is the weather in Asansol"` | Fetches real-time weather report (free via `wttr.in` or OpenWeather). |
| `"Open Chrome"` / `"Open VS Code"` | Launches the specified desktop application. |
| `"Open YouTube"` / `"Open GitHub"` | Opens the website in your default browser. |
| `"Play Iron Man theme on YouTube"` | Opens and plays the song/video on YouTube. |
| `"Search Google for Python AI"` | Performs a Google search in your browser. |
| `"Wikipedia Albert Einstein"` | Speaks a concise 2-sentence summary from Wikipedia. |
| `"Take a note: Buy new speakers"` | Appends timestamped note to `data/notes.txt`. |
| `"Read notes"` / `"Show my notes"` | Reads aloud your recent recorded notes. |
| `"Add todo: Build Iron Man suit"` | Adds task to `data/todo.json`. |
| `"List todo"` / `"My tasks"` | Reads aloud all pending to-do tasks. |
| `"Tell me a joke"` / `"Motivate me"` | Tells an AI joke or inspirational quote. |
| `"Who are you"` / `"Who made you"` | Explains JARVIS identity and capabilities. |

---

## 🔧 Customizing JARVIS Voice
In `.env` or `config.py`, you can change `EDGE_TTS_VOICE` to any supported neural voice:
- `en-GB-RyanNeural` — Authentic British Jarvis style voice (Default)
- `en-US-ChristopherNeural` — Deep American male voice
- `hi-IN-MadhurNeural` — Natural Hindi-English Hinglish voice

Enjoy your personal J.A.R.V.I.S. AI Assistant! ⚡
