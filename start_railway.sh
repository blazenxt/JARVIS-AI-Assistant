#!/usr/bin/env bash
set -e

echo "================================================================="
echo "  J.A.R.V.I.S. // STARTING LOCAL OFFLINE LLM & WEB HUD SERVER    "
echo "================================================================="

export AI_BACKEND=${AI_BACKEND:-"ollama"}
export OLLAMA_MODEL=${OLLAMA_MODEL:-"tinyllama"}
export OLLAMA_BASE_URL=${OLLAMA_BASE_URL:-"http://localhost:11434/v1"}

if [ "$AI_BACKEND" = "ollama" ]; then
    echo "[Ollama] Starting local offline Ollama AI daemon in background..."
    ollama serve > /tmp/ollama.log 2>&1 &
    
    echo "[Ollama] Waiting for Ollama server to initialize..."
    for i in {1..20}; do
        if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
            echo "[Ollama] Ollama server is ONLINE on port 11434!"
            break
        fi
        sleep 1
    done

    echo "[Ollama] Downloading/checking local offline LLM model '$OLLAMA_MODEL' (lightweight CPU-optimized)..."
    ollama pull "$OLLAMA_MODEL" || echo "[Ollama Warning] Could not pull model right now, will retry on demand."
fi

echo "[JARVIS] Launching Holographic Web HUD Server on port ${PORT:-8000}..."
exec python3 server.py
