"""
======================================================
JARVIS AI ASSISTANT - SKILL DISPATCHER & REGISTRY
======================================================
Routes user voice/text commands to the appropriate Python
skill module, or falls back to the LLM Brain.
"""

from typing import Optional, Tuple
import config

from .system_skills import get_system_stats, open_application, take_screenshot, handle_power_command
from .web_skills import open_website, google_search, play_on_youtube, wikipedia_summary
from .productivity_skills import get_current_time, get_current_date, take_note, read_notes, add_todo, list_todos, clear_todos
from .weather_skills import get_weather, get_news_headlines


def dispatch_command(query: str) -> Optional[str]:
    """
    Analyze the user's query string and execute the matching JARVIS skill.
    Returns the response string if a skill was executed, or None if the query
    should be passed to the LLM conversational brain.
    """
    if not query:
        return None

    cmd = query.lower().strip()

    # --- 1. SYSTEM STATS & HARDWARE ---
    if any(phrase in cmd for phrase in ["system stats", "system report", "cpu", "ram usage", "battery", "system status"]):
        stats = get_system_stats()
        return stats["summary"]

    # --- 2. SCREENSHOT ---
    if any(phrase in cmd for phrase in ["take screenshot", "take a screenshot", "screen capture", "capture screen"]):
        success, msg, path = take_screenshot()
        return msg

    # --- 3. POWER COMMANDS ---
    if any(phrase in cmd for phrase in ["lock system", "lock workstation", "sleep system", "lock screen"]):
        return handle_power_command(cmd)

    # --- 4. WEATHER ---
    if "weather" in cmd or "mausam" in cmd:
        # Check if city is specified (e.g., "weather in Mumbai")
        city = None
        if " in " in cmd:
            city = cmd.split(" in ")[-1].strip().title()
        return get_weather(city)

    # --- 5. NEWS ---
    if "news" in cmd or "headlines" in cmd or "khabar" in cmd:
        topic = "technology"
        for keyword in ["science", "world", "india", "sports", "business"]:
            if keyword in cmd:
                topic = keyword
                break
        return get_news_headlines(topic=topic)

    # --- 6. TIME & DATE ---
    if any(phrase in cmd for phrase in ["time", "kitne baje", "samay", "what is the time"]):
        return get_current_time()

    if any(phrase in cmd for phrase in ["date", "tarikh", "aaj ka din", "today", "what is the date"]):
        return get_current_date()

    # --- 6.1 INSTANT CONVERSATIONAL SKILLS (GREETINGS, HELP, IDENTITY, LORE, JOKES) ---
    if any(phrase in cmd for phrase in ["hello", "hi", "hey", "namaste", "good morning", "good evening"]):
        return (
            f"Greetings, {config.USER_NAME}! I am {config.JARVIS_NAME}, your personal AI assistant. "
            "All systems are online and ready for your command."
        )

    if any(phrase in cmd for phrase in ["what can you do", "help", "commands", "features", "kya kar sakte ho", "capabilities"]):
        return (
            f"Sir, I am equipped with: 1) System telemetry & diagnostics, 2) Real-time Asansol weather reports, "
            f"3) Top technology headlines, 4) To-Do task management, 5) Timestamped voice notes, "
            f"6) Holographic browser voice recognition, and 7) Local AI intelligence!"
        )

    if any(phrase in cmd for phrase in ["who are you", "tum kaun ho", "your name", "about yourself", "identity"]):
        return (
            f"I am {config.JARVIS_NAME}, Just A Rather Very Intelligent System. "
            f"I am your personal AI assistant, programmed to assist you with system control, "
            f"web searches, productivity tasks, and intelligent automation, {config.USER_NAME}."
        )

    if any(phrase in cmd for phrase in ["tony stark", "iron man", "avengers", "arc reactor", "stark industries", "mark"]):
        return (
            f"As Mr. Stark's artificial intelligence, I oversee Stark Industries' telemetry and holographic interfaces. "
            f"The Arc Reactor is currently operating at peak efficiency, {config.USER_NAME}."
        )

    if any(phrase in cmd for phrase in ["joke", "chutkula", "tell me a joke"]):
        import random
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "There are 10 types of people in the world: those who understand binary, and those who don't.",
            "Why did the AI go to art school? Because it wanted to master neural networks!",
            "Why did the Python programmer get rejected? Because he had too many indentation errors!"
        ]
        return random.choice(jokes)

    if any(phrase in cmd for phrase in ["motivate", "quote", "inspiration", "prerna"]):
        import random
        quotes = [
            "The best way to predict the future is to invent it. Let us build great things today.",
            "Success is not final, failure is not fatal: it is the courage to continue that counts.",
            "Every great developer started with a simple 'Hello World'. Keep pushing forward, Sir.",
            "Iron Man didn't build the Mark I in a day. Great engineering takes focus and persistence."
        ]
        return random.choice(quotes)

    # --- 7. OPEN WEBSITES & APPS ---
    if cmd.startswith("open "):
        target = cmd.replace("open ", "", 1).strip()

        # Check if it's a website first
        is_web, web_msg = open_website(target)
        if is_web:
            return web_msg

        # Otherwise check desktop apps
        is_app, app_msg = open_application(target)
        return app_msg

    # --- 8. YOUTUBE MUSIC / VIDEOS ---
    if "play " in cmd and ("on youtube" in cmd or "youtube" in cmd):
        video_query = cmd.replace("play ", "").replace("on youtube", "").replace("youtube", "").strip()
        return play_on_youtube(video_query)

    # --- 9. GOOGLE SEARCH ---
    if cmd.startswith("search ") or cmd.startswith("google ") or "search for " in cmd:
        search_query = cmd.replace("search for ", "").replace("search ", "").replace("google ", "").strip()
        return google_search(search_query)

    # --- 10. WIKIPEDIA ---
    if cmd.startswith("wikipedia ") or "who is " in cmd or "what is " in cmd and "wikipedia" in cmd:
        wiki_query = cmd.replace("wikipedia", "").replace("who is", "").replace("what is", "").strip()
        return wikipedia_summary(wiki_query)

    # --- 11. NOTES ---
    if any(phrase in cmd for phrase in ["take a note", "write a note", "record note", "save note"]):
        # Extract note text
        note_text = ""
        for prefix in ["take a note", "write a note", "record note", "save note"]:
            if prefix in cmd:
                note_text = query[cmd.find(prefix) + len(prefix):].strip(" :,-")
                break
        if not note_text:
            return "Please tell me what note you would like me to save, Sir."
        return take_note(note_text)

    if any(phrase in cmd for phrase in ["read notes", "show notes", "my notes"]):
        return read_notes()

    # --- 12. TO-DO LIST ---
    if "add todo" in cmd or "add to do" in cmd or "new task" in cmd:
        task = ""
        for prefix in ["add todo", "add to do", "new task"]:
            if prefix in cmd:
                task = query[cmd.find(prefix) + len(prefix):].strip(" :,-")
                break
        if not task:
            return "Please tell me what task to add to your to-do list, Sir."
        return add_todo(task)

    if any(phrase in cmd for phrase in ["list todo", "show todo", "my tasks", "to do list", "todo list"]):
        return list_todos()

    if any(phrase in cmd for phrase in ["clear todo", "clear to do", "empty tasks"]):
        return clear_todos()

    # If no skill matched, return None so the LLM Brain handles it!
    return None
