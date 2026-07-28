#!/usr/bin/env python3
"""
======================================================
JARVIS AI ASSISTANT - WEB HUD & API SERVER
======================================================
Serves the Sci-Fi Holographic Web Dashboard (HTML/CSS/JS)
and provides JSON REST endpoints for controlling JARVIS
from the browser.
"""

import os
import json
import socketserver
from http.server import SimpleHTTPRequestHandler
from urllib.parse import urlparse
from pathlib import Path

import config
from jarvis import JarvisAssistant, ASCII_BANNER
from skills import get_system_stats, list_todos, read_notes

# Initialize JARVIS instance in server/text-mode
jarvis_instance = JarvisAssistant(force_text_mode=True)

# Path to web UI directory
WEB_DIR = Path(__file__).parent / "web_ui"


class JarvisHTTPRequestHandler(SimpleHTTPRequestHandler):
    """
    HTTP Request Handler that routes /api requests to JARVIS Python backend,
    and serves frontend HTML/CSS/JS from web_ui/.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def _send_json_response(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)

        # --- API ENDPOINTS ---
        if parsed.path == "/api/status":
            stats = get_system_stats()
            status_summary = config.get_status_summary()
            self._send_json_response(200, {
                "status": "online",
                "stats": stats,
                "config": status_summary
            })
            return

        if parsed.path == "/api/todos":
            todos = list_todos()
            self._send_json_response(200, {"todos": todos})
            return

        if parsed.path == "/api/notes":
            notes = read_notes(limit=10)
            self._send_json_response(200, {"notes": notes})
            return

        if parsed.path == "/api/config":
            status_summary = config.get_status_summary()
            self._send_json_response(200, {
                "config": status_summary,
                "groq_key_set": bool(config.GROQ_API_KEY and "your_" not in config.GROQ_API_KEY),
                "gemini_key_set": bool(config.GEMINI_API_KEY and "your_" not in config.GEMINI_API_KEY)
            })
            return

        # Default static file server
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/command":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(content_length)
                payload = json.loads(post_data.decode("utf-8"))
                cmd = payload.get("command", "").strip()

                if not cmd:
                    self._send_json_response(400, {"error": "Empty command received."})
                    return

                # Execute command via JARVIS instance
                reply = jarvis_instance.process_query(cmd)

                self._send_json_response(200, {
                    "command": cmd,
                    "reply": reply,
                    "status": "success"
                })
            except Exception as e:
                self._send_json_response(500, {"error": str(e), "reply": f"Error executing command: {e}"})
            return

        if parsed.path == "/api/config":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(content_length)
                payload = json.loads(post_data.decode("utf-8"))

                updated = config.update_config_batch(payload)
                from brain import get_brain
                get_brain().reinit_clients()

                self._send_json_response(200, {
                    "status": "success",
                    "updated": updated,
                    "summary": config.get_status_summary(),
                    "reply": "System settings and API keys updated successfully, Sir."
                })
            except Exception as e:
                self._send_json_response(500, {"error": str(e)})
            return

        self._send_json_response(404, {"error": "Endpoint not found."})

    def log_message(self, format, *args):
        # Quiet server logs
        pass


class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


def start_web_server(host: str = config.WEB_HOST, port: int = config.WEB_PORT):
    """
    Start the JARVIS Web HUD Server.
    """
    print(ASCII_BANNER)
    print(f"{'='*62}")
    print(f"  J.A.R.V.I.S. HOLOGRAPHIC WEB HUD SERVER OPERATIONAL")
    print(f"  Dashboard URL : http://localhost:{port}")
    print(f"  API Endpoint  : http://localhost:{port}/api/command")
    print(f"{'='*62}\n")
    print(f"[{config.JARVIS_NAME}]: Web server is listening on port {port}. Press Ctrl+C to terminate.")

    with ThreadedHTTPServer((host, port), JarvisHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n[{config.JARVIS_NAME}]: Web server shutting down...")
            httpd.shutdown()


if __name__ == "__main__":
    start_web_server()
