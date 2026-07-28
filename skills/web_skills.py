"""
======================================================
JARVIS AI ASSISTANT - WEB & SEARCH SKILLS
======================================================
Handles internet searches, Wikipedia queries, opening websites,
and playing videos on YouTube.
"""

import os
import platform
import webbrowser
from typing import Tuple
import config

try:
    import wikipedia
    WIKIPEDIA_AVAILABLE = True
except Exception:
    WIKIPEDIA_AVAILABLE = False

PYWHATKIT_AVAILABLE = False
try:
    if platform.system() in ["Windows", "Darwin"] or os.environ.get("DISPLAY"):
        import pywhatkit
        PYWHATKIT_AVAILABLE = True
except Exception:
    PYWHATKIT_AVAILABLE = False


# Dictionary of popular websites
WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "github": "https://github.com",
    "chatgpt": "https://chat.openai.com",
    "openai": "https://www.openai.com",
    "whatsapp": "https://web.whatsapp.com",
    "instagram": "https://www.instagram.com",
    "linkedin": "https://www.linkedin.com",
    "reddit": "https://www.reddit.com",
    "twitter": "https://twitter.com",
    "x": "https://x.com",
    "netflix": "https://www.netflix.com",
    "amazon": "https://www.amazon.in",
    "flipkart": "https://www.flipkart.com",
    "stackoverflow": "https://stackoverflow.com",
}


def open_website(site_name: str) -> Tuple[bool, str]:
    """
    Open a website in the default browser.
    """
    clean_site = site_name.lower().strip()

    # Check against known sites
    for name, url in WEBSITES.items():
        if name in clean_site or clean_site in name:
            try:
                webbrowser.open(url)
                return True, f"Opening {name.title()} in your browser, Sir."
            except Exception as e:
                return False, f"Could not open browser: {e}"

    # If site is a domain or URL
    if "." in clean_site:
        url = clean_site if clean_site.startswith("http") else f"https://{clean_site}"
        try:
            webbrowser.open(url)
            return True, f"Opening {clean_site} in your browser."
        except Exception as e:
            return False, f"Could not open URL: {e}"

    return False, f"I am not familiar with the website '{site_name}'. Would you like me to Google it?"


def google_search(query: str) -> str:
    """
    Perform a Google search for the query in the default web browser.
    """
    if not query or not query.strip():
        return "Please specify what you would like me to search for on Google."

    clean_query = query.strip()
    search_url = f"https://www.google.com/search?q={clean_query}"

    try:
        webbrowser.open(search_url)
        return f"I have displayed Google search results for '{clean_query}', Sir."
    except Exception as e:
        return f"Failed to perform Google search: {e}"


def play_on_youtube(query: str) -> str:
    """
    Play a video or song on YouTube.
    Uses pywhatkit if available, or opens YouTube search directly.
    """
    if not query or not query.strip():
        return "Please specify what video or song you want me to play on YouTube."

    clean_query = query.strip()
    try:
        if PYWHATKIT_AVAILABLE:
            pywhatkit.playonyt(clean_query)
            return f"Playing '{clean_query}' on YouTube now, Sir."
        else:
            url = f"https://www.youtube.com/results?search_query={clean_query}"
            webbrowser.open(url)
            return f"Opening YouTube search for '{clean_query}', Sir."
    except Exception as e:
        return f"Could not play video on YouTube: {e}"


def wikipedia_summary(query: str, sentences: int = 2) -> str:
    """
    Fetch a concise Wikipedia summary for the requested topic.
    """
    if not query or not query.strip():
        return "Please specify the topic you want to look up on Wikipedia."

    if not WIKIPEDIA_AVAILABLE:
        return "Wikipedia library is not installed."

    try:
        summary = wikipedia.summary(query, sentences=sentences)
        return f"According to Wikipedia: {summary}"
    except wikipedia.exceptions.DisambiguationError as e:
        options = ", ".join(e.options[:3])
        return f"The topic '{query}' is ambiguous. Did you mean: {options}?"
    except wikipedia.exceptions.PageError:
        return f"I could not find a Wikipedia page matching '{query}'."
    except Exception as e:
        return f"An error occurred while searching Wikipedia: {e}"
