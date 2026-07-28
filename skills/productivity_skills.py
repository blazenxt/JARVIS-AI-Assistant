"""
======================================================
JARVIS AI ASSISTANT - PRODUCTIVITY SKILLS
======================================================
Handles notes, to-do lists, time, date, and reminders.
"""

import json
import datetime
from typing import List, Dict
import config


def get_current_time() -> str:
    """Return the current time in 12-hour format."""
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%I:%M %p')}, {config.USER_NAME}."


def get_current_date() -> str:
    """Return today's date formatted nicely."""
    now = datetime.datetime.now()
    return f"Today is {now.strftime('%A, %B %d, %Y')}, {config.USER_NAME}."


def take_note(note_text: str) -> str:
    """
    Save a note to data/notes.txt with a timestamp.
    """
    if not note_text or not note_text.strip():
        return "Sir, what would you like me to write down in your notes?"

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{now}] {note_text.strip()}\n"

    try:
        with open(config.NOTES_FILE, "a", encoding="utf-8") as f:
            f.write(entry)
        return f"I have recorded your note, Sir: '{note_text.strip()}'."
    except Exception as e:
        return f"Could not save your note: {e}"


def read_notes(limit: int = 3) -> str:
    """
    Read the most recent notes from data/notes.txt.
    """
    if not config.NOTES_FILE.exists():
        return "You have no notes recorded yet, Sir."

    try:
        with open(config.NOTES_FILE, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        if not lines:
            return "Your notes file is currently empty, Sir."

        recent_notes = lines[-limit:]
        formatted = " | ".join(recent_notes)
        return f"Here are your latest {len(recent_notes)} note entries: {formatted}"
    except Exception as e:
        return f"Failed to read notes: {e}"


def _load_todos() -> List[Dict]:
    if not config.TODO_FILE.exists():
        return []
    try:
        with open(config.TODO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_todos(todos: List[Dict]) -> bool:
    try:
        with open(config.TODO_FILE, "w", encoding="utf-8") as f:
            json.dump(todos, f, indent=4)
        return True
    except Exception:
        return False


def add_todo(task: str) -> str:
    """
    Add a new task to the to-do list.
    """
    if not task or not task.strip():
        return "Please specify the task you want me to add to your to-do list."

    todos = _load_todos()
    new_id = 1 if not todos else max(t.get("id", 0) for t in todos) + 1
    todos.append({
        "id": new_id,
        "task": task.strip(),
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "done": False
    })

    if _save_todos(todos):
        return f"I have added '{task.strip()}' to your to-do list, Sir."
    return "Failed to save task to to-do list."


def list_todos() -> str:
    """
    List all pending tasks in the to-do list.
    """
    todos = _load_todos()
    pending = [t for t in todos if not t.get("done", False)]

    if not pending:
        return f"You have no pending tasks in your to-do list, {config.USER_NAME}!"

    task_list = ", ".join(f"{i+1}. {t['task']}" for i, t in enumerate(pending))
    return f"You have {len(pending)} pending tasks: {task_list}."


def clear_todos() -> str:
    """
    Clear all completed or pending tasks from the to-do list.
    """
    _save_todos([])
    return "I have cleared your entire to-do list, Sir."
