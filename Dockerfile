# ==============================================================================
# J.A.R.V.I.S. // PRODUCTION DOCKERFILE WITH LOCAL OFFLINE OLLAMA LLM SUPPORT
# ==============================================================================
FROM python:3.11-slim

# Install system dependencies & curl for official Ollama installation
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    procps \
    gcc \
    zstd \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Install official Ollama Linux binaries
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy JARVIS application code & start scripts
COPY . .
RUN chmod +x start_railway.sh

# Default environment variables for Offline Ollama LLM
ENV AI_BACKEND=ollama
ENV OLLAMA_MODEL=tinyllama
ENV OLLAMA_BASE_URL=http://localhost:11434/v1
ENV PORT=8000

# Expose Web Dashboard and local Ollama port
EXPOSE 8000 11434

# Start both Ollama offline daemon and JARVIS web server
CMD ["./start_railway.sh"]
