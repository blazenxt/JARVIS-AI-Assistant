# 🤖 J.A.R.V.I.S. AI Assistant - Step-by-Step Hindi & Hinglish Setup Guide
### Aapka Apna Iron Man JARVIS Assistant (Python + Holographic Web HUD)

Namaste Sir (**User**)!
Aapne kaha **"Meko jarvis banana hain"** — aur ab aapka complete, modular, aur futuristic **J.A.R.V.I.S. AI Assistant Suite** tayyar hai! 

Ye project sirf ek basic script nahi hai, balki ek **Production-Ready Multi-Modal Assistant** hai jo aapki aawaz sunkar computer control kar sakta hai, web search kar sakta hai, weather aur news bata sakta hai, to-do list aur notes maintain kar sakta hai, aur **Iron Man ke Arc Reactor jaise Holographic Web HUD Dashboard** ke sath aata hai!

---

## 🌟 JARVIS ke Main Features (Kya Kya Kar Sakta Hai?)

1. **Aawaz Sunna aur Bolna (Voice & Speech)**:
   - Microphone se **English, Hindi, aur Hinglish** commands sunta hai (`en-IN` support).
   - Agar microphone na ho (ya aap terminal me test kar rahe hon), toh automatic **keyboard text typing** mode me chala jata hai!
   - Microsoft Edge ke Natural AI Neural Voices (`edge-tts`) use karta hai jisse aawaz bilkul sci-fi JARVIS jaisi aati hai.

2. **Smart AI Brain (LLM Intelligence)**:
   - **Groq API** (Free & Super Fast Llama-3 AI)
   - **Google Gemini API** (Free Gemini AI)
   - **OpenAI API** (GPT-4o)
   - **Offline Mode**: Agar koi API key na ho, tab bhi JARVIS crash nahi hota! Smart offline rules ke zariye time, date, jokes, motivation, aur system commands par automatically jawab deta hai.

3. **System Control & Automation Skills**:
   - `System Stats`: CPU usage %, RAM %, aur Battery check karta hai (`psutil`).
   - `Open Apps`: Chrome, VS Code, Notepad, Calculator, Terminal jaise apps open karta hai.
   - `Screenshot`: Automatic screen capture karke `data/screenshots/` folder me save karta hai.
   - `Weather & News`: **Bina kisi API key ke** Asansol ya kisi bhi shahar ka mausam (`wttr.in`) aur latest khabar batata hai!
   - `Productivity`: Aawaz se Notes likhna aur To-Do List me tasks add karna.

4. **Sci-Fi Iron Man Web HUD Dashboard**:
   - Web browser me **`http://localhost:8000`** par ek glowing cyan & gold Holographic Dashboard chalta hai!
   - Live CPU/RAM gauges, animated Arc Reactor, aur built-in Browser Speech Recognition.

---

## 🚂 Railway.app Par 2 Minute Me Kaise Deploy Karein (Offline Ollama LLM + Web HUD)

Aap apne JARVIS Web HUD ko **Railway.app** cloud par host kar sakte hain jahan humne **Official Dockerfile ke zariye Local Offline Ollama LLM (`tinyllama`)** ka support daal diya hai! Ab bina kisi external API key ke bhi cloud container ke andar hi asli AI model chalega:

### Step 1: Railway.app Par Login Karein
1. **[https://railway.app](https://railway.app)** par jayein aur apne GitHub account (`@blazenxt`) se login karein.
2. **"New Project"** button par click karein -> **"Deploy from GitHub repo"** select karein.
3. Apna repository select karein: **`blazenxt/JARVIS-AI-Assistant`**.

### Step 2: Automatic Docker Build (Ollama LLM Included!)
- Railway automatically hamara naya **`Dockerfile`** use karega jisme **Ollama Linux Daemon** aur **`tinyllama` offline AI model** configured hai.
- Aapko koi bhi API key lagane ki zaroorat nahi hai! Default backend automatic `AI_BACKEND=ollama` chalega.

### Step 3: Public URL Open Karein!
1. **Settings -> Networking** tab me jaakar **"Generate Domain"** par click karein.
2. Railway aapko ek public link dega (jaise `https://jarvis-ai-assistant.up.railway.app`).
3. Is link ko apne **Mobile ya PC ke Chrome Browser** me open karein!
4. **"ACTIVATE VOICE (HEY JARVIS)"** button press karke aawaz se command dein — JARVIS aapke browser me wapas bolega! 🎉

---

## 🚀 Step-by-Step Local Installation & Run Guide (PC / Laptop / Termux)

### Step 1: Terminal Open Karein
Aapke folder me jaakar terminal open karein:
```bash
cd /path/to/jarvis
```

### Step 2: Python Libraries Install Karein
Saari zaroori libraries install karne ke liye ye command chalayein:
```bash
pip install -r requirements.txt
```
> **Windows Users ke liye Note (Microphone Audio):**
> Agar Windows par `pyaudio` install karne me koi error aaye, toh ye commands chalayein:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### Step 3: Free AI API Key Lagayein (.env File Configuration)
1. Project me `.env.example` file ki copy banakar `.env` naam ki file banayein:
   ```bash
   cp .env.example .env
   ```
2. Ab `.env` file ko open karein aur apna **Free API Key** daalein:
   - **Groq API (Recommended)**: [https://console.groq.com/keys](https://console.groq.com/keys) par jaakar free account banayein aur key ko `GROQ_API_KEY=` ke aage paste karein.
   - **Google Gemini API**: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) par jaakar key le sakte hain.
3. Agar aapke paas abhi koi key nahi hai, toh chinta mat karein! JARVIS default **offline smart rules** se kaam karega.

---

## 🖥️ JARVIS ko Kaise Chalayein (Run Modes)

### Mode 1: Interactive Terminal Mode (Default)
Simple command chalayein, aur JARVIS aawaz / text commands sunne ke liye tayyar ho jayega:
```bash
python3 jarvis.py
```
> **Tip**: Agar aap bina microphone ke sirf typing se baat karna chahte hain, toh `python3 jarvis.py --text-only` use karein.

### Mode 2: Sci-Fi Web HUD Dashboard (Iron Man Mode! 🔥)
Apne browser me holographic interface aur animated Arc Reactor dekhne ke liye:
```bash
python3 jarvis.py --mode web
# ya phir directly:
python3 server.py
```
Ab apne browser me open karein:
👉 **`http://localhost:8000`**

Wahan aapko:
- Glowing cyan Arc Reactor animation dikhegi!
- Live CPU / RAM system telemetry gauges dikhenge!
- Clickable quick-command buttons (Weather, Stats, Notes, To-Do, Joke) milenge!
- Browser ke Microphone icon par click karke aap direct bol kar command de sakte hain!

### Mode 3: Automated Testing (Test Suite)
Check karne ke liye ki sab kuch perfectly kaam kar raha hai:
```bash
python3 jarvis.py --test
```

---

## 🗣️ Aap JARVIS Se Kya Kya Bol / Puch Sakte Hain?

| Aapka Command (English ya Hinglish) | JARVIS Kya Karega |
| :--- | :--- |
| `"System stats"` / `"CPU kaisa hai"` | System ka live CPU %, RAM usage, aur Battery status batayega. |
| `"What is the weather in Asansol"` | Asansol (ya kisi bhi city) ka real-time mausam batayega. |
| `"Open Chrome"` / `"Open Notepad"` | Aapke computer me Chrome browser ya Notepad open karega. |
| `"Open YouTube"` / `"Open GitHub"` | Default browser me website open karega. |
| `"Play Iron Man theme on YouTube"` | YouTube par song/video search karke chala dega. |
| `"Search for Python AI on Google"` | Google par topic search karega. |
| `"Wikipedia Albert Einstein"` | Wikipedia se topic ka 2 line summary sunayega. |
| `"Take a note: Buy new laptop"` | Aapke note ko `data/notes.txt` me date & time ke sath save karega. |
| `"Read notes"` / `"Show my notes"` | Aapke save kiye gaye notes padh kar sunayega. |
| `"Add todo: Build Iron Man suit"` | Aapki To-Do list me naya task add karega. |
| `"List todo"` | Pending to-do tasks batayega. |
| `"Tell me a joke"` / `"Motivate me"` | Chutkula ya motivational quote sunayega. |
| `"Who are you"` / `"Tum kaun ho"` | Apna introduction aur capabilities batayega. |

---

## ⚡ Voice Accent / Aawaz Change Karna
Agar aap chahte hain ki JARVIS ki aawaz British style ke bajaye **Hinglish / Indian accent** me ho, toh `.env` ya `config.py` me set karein:
- **British JARVIS (Default)**: `EDGE_TTS_VOICE=en-GB-RyanNeural`
- **Indian English / Hindi Accent**: `EDGE_TTS_VOICE=hi-IN-MadhurNeural`
- **American Male Voice**: `EDGE_TTS_VOICE=en-US-ChristopherNeural`

**Badhai ho Sir! Aapka apna J.A.R.V.I.S. AI Assistant tayyar hai!** 🎉
