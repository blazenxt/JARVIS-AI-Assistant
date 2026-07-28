"""
======================================================
JARVIS AI ASSISTANT - WEATHER & NEWS SKILLS
======================================================
Fetches live weather reports (using OpenWeather or wttr.in)
and top news headlines.
"""

import requests
from typing import Optional
import config


def get_weather(city: Optional[str] = None) -> str:
    """
    Get current weather report for a given city.
    Uses OpenWeatherMap if API key is provided, otherwise uses wttr.in free service.
    """
    target_city = city if city else config.DEFAULT_CITY

    # 1. Try OpenWeatherMap if key is provided
    if config.OPENWEATHER_API_KEY and "your_" not in config.OPENWEATHER_API_KEY:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={target_city}&appid={config.OPENWEATHER_API_KEY}&units=metric"
            res = requests.get(url, timeout=5).json()
            if res.get("cod") == 200:
                temp = round(res["main"]["temp"])
                desc = res["weather"][0]["description"]
                humidity = res["main"]["humidity"]
                return (
                    f"The current weather in {target_city} is {desc} with a temperature of "
                    f"{temp} degrees Celsius and humidity at {humidity} percent."
                )
        except Exception as e:
            print(f"[OpenWeather Error] {e} -> Switching to free wttr.in")

    # 2. Try wttr.in free API (No API Key Required!)
    try:
        url = f"https://wttr.in/{target_city}?format=%C+%t+(Humidity:+%h)"
        res = requests.get(url, timeout=5)
        if res.status_code == 200 and res.text:
            return f"The current weather in {target_city} is: {res.text.strip()}."
    except Exception as e:
        print(f"[Weather API Error] {e}")

    return f"I am unable to retrieve the weather report for {target_city} at this time, Sir."


def get_news_headlines(topic: str = "technology", count: int = 3) -> str:
    """
    Get latest top headlines using free public feeds or fallback summaries.
    """
    try:
        # We can use Google News RSS or public free JSON endpoint
        url = f"https://api.rss2json.com/v1/api.json?rss_url=https://news.google.com/rss/search?q={topic}&hl=en-IN&gl=IN&ceid=IN:en"
        res = requests.get(url, timeout=5).json()

        if res.get("status") == "ok" and res.get("items"):
            items = res["items"][:count]
            headlines = [f"{i+1}. {item['title'].split(' - ')[0]}" for i, item in enumerate(items)]
            joined = " | ".join(headlines)
            return f"Here are the top {count} headlines regarding {topic}: {joined}"
    except Exception as e:
        print(f"[News API Error] {e}")

    return (
        f"I am unable to fetch live news feeds at this moment, Sir. "
        "Please check your internet connection or try again later."
    )
