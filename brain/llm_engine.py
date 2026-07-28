"""
======================================================
JARVIS AI ASSISTANT - INTELLIGENCE BRAIN (LLM ENGINE)
======================================================
Handles natural language reasoning and conversation using
Groq, Google Gemini, OpenAI, Ollama, or Smart Offline rules.
"""

import datetime
import random
from typing import List, Dict
import config

# Try importing LLM client libraries
import warnings
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


JARVIS_SYSTEM_PROMPT = f"""You are {config.JARVIS_NAME} (Just A Rather Very Intelligent System), an elite, highly intelligent, and polite AI assistant assisting {config.USER_NAME}.
Your characteristics:
1. Concise, witty, articulate, and reliable—like Tony Stark's JARVIS.
2. Address the user respectfully as '{config.USER_NAME}' when appropriate.
3. Keep answers spoken-voice friendly: clear, direct, and avoiding complex markdown tables or excessive bullet lists unless explicitly asked.
4. If asked about today's date, remember that you are operating in real-time and always be helpful.
5. Answer in the same language style as the user (English, Hindi, or Hinglish).
"""


class LLMEngine:
    """
    JARVIS Intelligence Center: Switches between LLM backends and maintains chat history.
    """

    def __init__(self, backend: str = config.AI_BACKEND):
        self.backend = backend.lower()
        self.history: List[Dict[str, str]] = []
        self._init_clients()

    def _init_clients(self):
        """Initialize API clients based on available keys."""
        self.groq_client = None
        self.openai_client = None
        self.gemini_model = None

        # Groq
        if GROQ_AVAILABLE and config.GROQ_API_KEY and "your_" not in config.GROQ_API_KEY:
            try:
                self.groq_client = Groq(api_key=config.GROQ_API_KEY)
            except Exception as e:
                print(f"[Brain] Groq init warning: {e}")

        # Gemini
        if GEMINI_AVAILABLE and config.GEMINI_API_KEY and "your_" not in config.GEMINI_API_KEY:
            try:
                genai.configure(api_key=config.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel(config.GEMINI_MODEL)
            except Exception as e:
                print(f"[Brain] Gemini init warning: {e}")

        # OpenAI
        if OPENAI_AVAILABLE and config.OPENAI_API_KEY and "your_" not in config.OPENAI_API_KEY:
            try:
                self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
            except Exception as e:
                print(f"[Brain] OpenAI init warning: {e}")

    def ask(self, prompt: str, clear_history: bool = False) -> str:
        """
        Send user query to the active AI backend and return a response.
        """
        if not prompt or not prompt.strip():
            return "I am listening, Sir."

        if clear_history:
            self.history.clear()

        # Try configured backend
        response = ""
        if self.backend == "groq" and self.groq_client:
            response = self._ask_groq(prompt)
        elif self.backend == "gemini" and self.gemini_model:
            response = self._ask_gemini(prompt)
        elif self.backend == "openai" and self.openai_client:
            response = self._ask_openai(prompt)
        elif self.backend == "ollama" and OPENAI_AVAILABLE:
            response = self._ask_ollama(prompt)

        # Fallback if selected API failed or is not configured
        if not response:
            # Try Groq -> Gemini -> OpenAI as auto-fallbacks
            if self.groq_client and self.backend != "groq":
                response = self._ask_groq(prompt)
            elif self.gemini_model and self.backend != "gemini":
                response = self._ask_gemini(prompt)
            elif self.openai_client and self.backend != "openai":
                response = self._ask_openai(prompt)
            else:
                response = self._ask_smart_offline(prompt)

        return response.strip()

    def _ask_groq(self, prompt: str) -> str:
        try:
            messages = [{"role": "system", "content": JARVIS_SYSTEM_PROMPT}]
            messages.extend(self.history[-8:]) # keep last 4 turns
            messages.append({"role": "user", "content": prompt})

            completion = self.groq_client.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            reply = completion.choices[0].message.content
            self._update_history(prompt, reply)
            return reply
        except Exception as e:
            print(f"[Groq API Error] {e}")
            return ""

    def _ask_gemini(self, prompt: str) -> str:
        try:
            full_prompt = f"{JARVIS_SYSTEM_PROMPT}\n\nUser: {prompt}\nJARVIS:"
            res = self.gemini_model.generate_content(full_prompt)
            reply = res.text
            self._update_history(prompt, reply)
            return reply
        except Exception as e:
            print(f"[Gemini API Error] {e}")
            return ""

    def _ask_openai(self, prompt: str) -> str:
        try:
            messages = [{"role": "system", "content": JARVIS_SYSTEM_PROMPT}]
            messages.extend(self.history[-8:])
            messages.append({"role": "user", "content": prompt})

            completion = self.openai_client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            reply = completion.choices[0].message.content
            self._update_history(prompt, reply)
            return reply
        except Exception as e:
            print(f"[OpenAI API Error] {e}")
            return ""

    def _ask_ollama(self, prompt: str) -> str:
        try:
            client = OpenAI(base_url=config.OLLAMA_BASE_URL, api_key="ollama")
            messages = [{"role": "system", "content": JARVIS_SYSTEM_PROMPT}]
            messages.extend(self.history[-6:])
            messages.append({"role": "user", "content": prompt})

            completion = client.chat.completions.create(
                model=config.OLLAMA_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=400
            )
            reply = completion.choices[0].message.content
            self._update_history(prompt, reply)
            return reply
        except Exception as e:
            print(f"[Ollama Error] {e}")
            return ""

    def _ask_smart_offline(self, prompt: str) -> str:
        """
        Smart Rule-Based Fallback when no LLM API is connected.
        Ensures JARVIS remains intelligent and interactive out of the box!
        """
        query = prompt.lower().strip()
        now = datetime.datetime.now()

        if any(word in query for word in ["who are you", "tum kaun ho", "your name", "about yourself", "identity"]):
            return (
                f"I am {config.JARVIS_NAME}, Just A Rather Very Intelligent System. "
                f"I am your personal AI assistant, programmed to assist you with system control, "
                f"web searches, productivity tasks, and intelligent automation, {config.USER_NAME}."
            )

        if any(word in query for word in ["how are you", "kaise ho", "kya haal"]):
            replies = [
                f"All systems are fully operational and running at peak performance, {config.USER_NAME}.",
                f"I am doing excellent, {config.USER_NAME}. Ready for your commands.",
                f"My neural networks are calibrated and ready to assist you, Sir."
            ]
            return random.choice(replies)

        if any(word in query for word in ["who created you", "who made you", "kisne banaya"]):
            return (
                f"I was created as an advanced multi-modal AI assistant to serve {config.USER_NAME}. "
                f"My architecture combines modular Python skills with a futuristic Web HUD interface."
            )

        if any(word in query for word in ["time", "kitne baje", "samay"]):
            current_time = now.strftime("%I:%M %p")
            return f"The current time is {current_time}, {config.USER_NAME}."

        if any(word in query for word in ["date", "tarikh", "aaj ka din", "today"]):
            current_date = now.strftime("%A, %B %d, %Y")
            return f"Today is {current_date}, {config.USER_NAME}."

        if any(word in query for word in ["joke", "chutkula"]):
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "There are 10 types of people in the world: those who understand binary, and those who don't.",
                "Why did the AI go to art school? Because it wanted to master neural networks!",
                "Why did the Python programmer get rejected? Because he had too many indentation errors!"
            ]
            return random.choice(jokes)

        if any(word in query for word in ["motivate", "quote", "inspiration", "prerna"]):
            quotes = [
                "The best way to predict the future is to invent it. Let us build great things today.",
                "Success is not final, failure is not fatal: it is the courage to continue that counts.",
                "Every great developer started with a simple 'Hello World'. Keep pushing forward, Sir.",
                "Iron Man didn't build the Mark I in a day. Great engineering takes focus and persistence."
            ]
            return random.choice(quotes)

        if any(word in query for word in ["thank", "shukriya", "dhanyavad"]):
            return f"You are always welcome, {config.USER_NAME}. I am here whenever you need me."

        # Default smart conversational reply
        return (
            f"I heard: '{prompt}'. While my cloud LLM API is currently offline or not configured in .env, "
            f"you can add a free Groq or Gemini API key to unlock my full generative intelligence, {config.USER_NAME}!"
        )

    def _update_history(self, user_msg: str, jarvis_msg: str):
        self.history.append({"role": "user", "content": user_msg})
        self.history.append({"role": "assistant", "content": jarvis_msg})
        if len(self.history) > 12:
            self.history = self.history[-12:]


# Global singleton
_brain_singleton = None

def get_brain() -> LLMEngine:
    global _brain_singleton
    if _brain_singleton is None:
        _brain_singleton = LLMEngine()
    return _brain_singleton
