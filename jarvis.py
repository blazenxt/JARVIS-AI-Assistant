#!/usr/bin/env python3
"""
=============================================================================
           J.A.R.V.I.S. - JUST A RATHER VERY INTELLIGENT SYSTEM
=============================================================================
A Modular, Production-Ready Python Voice & AI Assistant Suite with Sci-Fi UI
Created for Sir {config.USER_NAME}
=============================================================================
"""

import os
import sys
import time
import argparse
from typing import Optional

import config
from speech import get_tts_engine, get_speech_engine, speak
from brain import get_brain
from skills import dispatch_command, get_system_stats


ASCII_BANNER = r"""
     ██╗  █████╗  ██████╗  ██╗   ██╗ ██╗ ███████╗
     ██║ ██╔══██╗ ██╔══██╗ ██║   ██║ ██║ ██╔════╝
     ██║ ███████║ ██████╔╝ ██║   ██║ ██║ ███████╗
██   ██║ ██╔══██║ ██╔══██╗ ╚██╗ ██╔╝ ██║ ╚════██║
╚██████╔╝ ██║  ██║ ██║  ██║  ╚████╔╝  ██║ ███████║
 ╚═════╝  ╚═╝  ╚═╝ ╚═╝  ╚═╝   ╚═══╝   ╚═╝ ╚══════╝
      JUST A RATHER VERY INTELLIGENT SYSTEM
"""


class JarvisAssistant:
    """
    Main Controller for JARVIS AI Assistant.
    Coordinates Speech Input, Skill Execution, AI Reasoning, and Output.
    """

    def __init__(self, language: str = "en-IN", force_text_mode: bool = False):
        self.language = language
        self.force_text_mode = force_text_mode
        self.tts = get_tts_engine()
        self.ear = get_speech_engine(language=self.language)
        self.brain = get_brain()

        # Connect callbacks for status monitoring
        self.current_status = "STANDBY"
        self.ear.on_listen_status = self._set_status

    def _set_status(self, status: str):
        self.current_status = status

    def greet_user(self):
        """Greet the user upon startup."""
        print(ASCII_BANNER)
        print(f"{'='*62}")
        print(f"  User: {config.USER_NAME} | Backend: {config.AI_BACKEND.upper()} | City: {config.DEFAULT_CITY}")
        print(f"  Microphone Available: {self.ear.mic_available} | Text Fallback: {self.force_text_mode or not self.ear.mic_available}")
        print(f"{'='*62}\n")

        greeting = (
            f"Good day, {config.USER_NAME}. I am {config.JARVIS_NAME}. "
            "All core modules, system diagnostics, and neural networks are online and ready for your command."
        )
        speak(greeting)

    def process_query(self, query: str) -> str:
        """
        Process a single user query:
        1. Check if it's an exit command.
        2. Check if a JARVIS Skill matches.
        3. Otherwise, consult the LLM Brain.
        """
        if not query or not query.strip():
            return ""

        clean_query = query.strip()

        # 1. Check for shutdown / exit commands
        if any(phrase in clean_query.lower() for phrase in ["exit", "quit", "shutdown jarvis", "bye jarvis", "goodbye"]):
            farewell = f"Powering down JARVIS systems. Goodbye, {config.USER_NAME}."
            speak(farewell)
            sys.exit(0)

        # 2. Dispatch to modular skills
        self._set_status("PROCESSING")
        skill_response = dispatch_command(clean_query)

        if skill_response is not None:
            self._set_status("SPEAKING")
            speak(skill_response)
            self._set_status("STANDBY")
            return skill_response

        # 3. Fallback to LLM AI Brain
        brain_response = self.brain.ask(clean_query)
        self._set_status("SPEAKING")
        speak(brain_response)
        self._set_status("STANDBY")
        return brain_response

    def run_interactive_loop(self):
        """
        Main interactive loop for text/voice commands.
        """
        self.greet_user()

        while True:
            try:
                # Capture command from microphone or keyboard
                query = self.ear.listen(
                    prompt=f"Awaiting command, {config.USER_NAME}...",
                    force_text_mode=self.force_text_mode
                )
                if query:
                    self.process_query(query)
            except KeyboardInterrupt:
                print(f"\n[{config.JARVIS_NAME}]: Interrupted by user. Shutting down...")
                break
            except Exception as e:
                print(f"\n[JARVIS Loop Error]: {e}")
                time.sleep(1)

    def run_voice_wake_loop(self):
        """
        Voice Wake-Word mode: Continuously listens for 'Jarvis', then captures command.
        """
        self.greet_user()
        print(f"\n[{config.JARVIS_NAME}]: Running in continuous Voice Wake-Word mode.")

        while True:
            try:
                detected = self.ear.wait_for_wake_word()
                if detected:
                    speak(f"Yes, {config.USER_NAME}?")
                    query = self.ear.listen(prompt="Listening for your command...", force_text_mode=False)
                    if query:
                        self.process_query(query)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"\n[Wake-Word Error]: {e}")
                time.sleep(1)


def run_tests():
    """
    Run automated sanity test of JARVIS components.
    """
    print(ASCII_BANNER)
    print("======================================================")
    print("      JARVIS AI ASSISTANT - AUTOMATED TEST SUITE     ")
    print("======================================================\n")

    assistant = JarvisAssistant(force_text_mode=True)

    test_queries = [
        "who are you",
        "what is the time",
        "system stats",
        "weather in Asansol",
        "add todo build Iron Man suit",
        "list todo",
        "tell me a joke"
    ]

    for q in test_queries:
        print(f"\n--- Testing Query: '{q}' ---")
        reply = assistant.process_query(q)
        print(f"Result: {reply[:100]}..." if len(reply) > 100 else f"Result: {reply}")
        time.sleep(0.5)

    print("\n======================================================")
    print("      ALL TEST QUERIES COMPLETED SUCCESSFULLY!        ")
    print("======================================================")


def main():
    parser = argparse.ArgumentParser(description="J.A.R.V.I.S. AI Voice Assistant Suite")
    parser.add_argument("--mode", choices=["cli", "voice", "web"], default="cli",
                        help="Mode to run: cli (interactive text/voice), voice (wake-word loop), or web (Web HUD dashboard)")
    parser.add_argument("--text-only", action="store_true",
                        help="Force keyboard/CLI input even if microphone is available")
    parser.add_argument("--test", action="store_true",
                        help="Run automated sanity test of JARVIS skills and brain")

    args = parser.parse_args()

    if args.test:
        run_tests()
        return

    if args.mode == "web":
        print(f"\n[{config.JARVIS_NAME}]: Launching Sci-Fi Web HUD Server...")
        from server import start_web_server
        start_web_server()
        return

    assistant = JarvisAssistant(
        language="en-IN",
        force_text_mode=args.text_only
    )

    if args.mode == "voice":
        assistant.run_voice_wake_loop()
    else:
        assistant.run_interactive_loop()


if __name__ == "__main__":
    main()
