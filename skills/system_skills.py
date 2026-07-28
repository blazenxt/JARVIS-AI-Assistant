"""
======================================================
JARVIS AI ASSISTANT - SYSTEM & HARDWARE SKILLS
======================================================
Controls system hardware, checks CPU/RAM/Battery stats,
opens desktop applications, and captures screenshots.
"""

import os
import sys
import time
import platform
import subprocess
from pathlib import Path
from typing import Dict, Tuple
import config

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False


def get_system_stats() -> Dict[str, str]:
    """
    Get CPU, RAM, and Battery statistics.
    Returns dictionary with numerical & human-readable text.
    """
    stats = {
        "cpu_percent": "N/A",
        "ram_percent": "N/A",
        "ram_used_gb": "N/A",
        "ram_total_gb": "N/A",
        "battery_percent": "N/A",
        "battery_plugged": "Unknown",
        "summary": "System statistics are currently unavailable."
    }

    if not PSUTIL_AVAILABLE:
        return stats

    try:
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        mem_used = round(mem.used / (1024 ** 3), 1)
        mem_total = round(mem.total / (1024 ** 3), 1)

        stats["cpu_percent"] = f"{cpu}%"
        stats["ram_percent"] = f"{mem.percent}%"
        stats["ram_used_gb"] = f"{mem_used} GB"
        stats["ram_total_gb"] = f"{mem_total} GB"

        battery_info = ""
        try:
            battery = psutil.sensors_battery()
            if battery:
                stats["battery_percent"] = f"{round(battery.percent)}%"
                stats["battery_plugged"] = "Plugged In" if battery.power_plugged else "On Battery"
                battery_info = f", and battery is at {round(battery.percent)}% ({stats['battery_plugged']})"
        except Exception:
            pass

        stats["summary"] = (
            f"CPU utilization is at {cpu}%. "
            f"Memory usage is {mem.percent}% ({mem_used} of {mem_total} gigabytes){battery_info}."
        )
    except Exception as e:
        print(f"[System Stats Error] {e}")

    return stats


def open_application(app_name: str) -> Tuple[bool, str]:
    """
    Open common desktop applications across Windows, macOS, and Linux.
    """
    app_clean = app_name.lower().strip()
    os_name = platform.system().lower()

    # Dictionary mapping common app names to OS commands
    app_map = {
        "chrome": {
            "windows": "start chrome",
            "darwin": "open -a 'Google Chrome'",
            "linux": "google-chrome &"
        },
        "notepad": {
            "windows": "notepad.exe",
            "darwin": "open -a 'TextEdit'",
            "linux": "gedit &"
        },
        "calculator": {
            "windows": "calc.exe",
            "darwin": "open -a 'Calculator'",
            "linux": "gnome-calculator &"
        },
        "vs code": {
            "windows": "code",
            "darwin": "open -a 'Visual Studio Code'",
            "linux": "code &"
        },
        "vscode": {
            "windows": "code",
            "darwin": "open -a 'Visual Studio Code'",
            "linux": "code &"
        },
        "explorer": {
            "windows": "explorer.exe",
            "darwin": "open .",
            "linux": "xdg-open . &"
        },
        "file manager": {
            "windows": "explorer.exe",
            "darwin": "open .",
            "linux": "xdg-open . &"
        },
        "cmd": {
            "windows": "start cmd",
            "darwin": "open -a 'Terminal'",
            "linux": "gnome-terminal &"
        },
        "terminal": {
            "windows": "start cmd",
            "darwin": "open -a 'Terminal'",
            "linux": "gnome-terminal &"
        }
    }

    # Find closest matching app
    target_cmd = None
    matched_app = app_clean

    for key, cmds in app_map.items():
        if key in app_clean or app_clean in key:
            matched_app = key
            if "windows" in os_name:
                target_cmd = cmds.get("windows")
            elif "darwin" in os_name:
                target_cmd = cmds.get("darwin")
            else:
                target_cmd = cmds.get("linux")
            break

    if not target_cmd:
        # Try generic system launcher
        try:
            if "windows" in os_name:
                os.system(f"start {app_clean}")
            elif "darwin" in os_name:
                os.system(f"open -a '{app_clean}'")
            else:
                os.system(f"{app_clean} &")
            return True, f"Attempting to launch {app_name}."
        except Exception:
            return False, f"I could not locate an application named {app_name}."

    try:
        subprocess.Popen(target_cmd, shell=True)
        return True, f"Opening {matched_app.title()}, Sir."
    except Exception as e:
        return False, f"Failed to launch {matched_app}: {e}"


def take_screenshot() -> Tuple[bool, str, str]:
    """
    Take a screen capture and save it in data/screenshots/.
    Returns (success, message, filepath).
    """
    screenshot_dir = config.DATA_DIR / "screenshots"
    screenshot_dir.mkdir(exist_ok=True)
    filename = f"screenshot_{int(time.time())}.png"
    filepath = screenshot_dir / filename

    if not PYAUTOGUI_AVAILABLE:
        return False, "PyAutoGUI library is not available for screenshots.", ""

    try:
        img = pyautogui.screenshot()
        img.save(str(filepath))
        return True, f"Screenshot captured and saved to {filename}.", str(filepath)
    except Exception as e:
        return False, f"Could not capture screenshot: {e}", ""


def handle_power_command(command: str) -> str:
    """
    Handle system power commands (lock, sleep, warning for shutdown/restart).
    """
    cmd = command.lower()
    os_name = platform.system().lower()

    if "lock" in cmd:
        try:
            if "windows" in os_name:
                os.system("rundll32.exe user32.dll,LockWorkStation")
            elif "darwin" in os_name:
                os.system("pmset displaysleepnow")
            else:
                os.system("xdg-screensaver lock")
            return "Locking workstation now, Sir."
        except Exception as e:
            return f"Failed to lock workstation: {e}"

    elif "sleep" in cmd:
        try:
            if "windows" in os_name:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            elif "darwin" in os_name:
                os.system("pmset sleepnow")
            else:
                os.system("systemctl suspend")
            return "Putting system to sleep."
        except Exception as e:
            return f"Failed to enter sleep mode: {e}"

    elif "shutdown" in cmd or "restart" in cmd or "reboot" in cmd:
        return "For your security, please perform system shutdown or reboot manually from your OS menu."

    return "Power command unrecognized."
