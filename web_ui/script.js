/* =========================================================
   J.A.R.V.I.S. // HOLOGRAPHIC SCI-FI CLIENT SCRIPT
   ========================================================= */

// DOM Elements
const statusText = document.getElementById("statusText");
const statusDot = document.getElementById("statusDot");
const reactorState = document.getElementById("reactorState");
const arcReactor = document.getElementById("arcReactor");
const chatLog = document.getElementById("chatLog");
const commandInput = document.getElementById("commandInput");
const hudClock = document.getElementById("hudClock");
const micBtn = document.getElementById("micBtn");
const cpuVal = document.getElementById("cpuVal");
const ramVal = document.getElementById("ramVal");
const backendVal = document.getElementById("backendVal");
const locVal = document.getElementById("locVal");
const browserTtsToggle = document.getElementById("browserTtsToggle");

let isListening = false;
let speechRecognizer = null;

// --- 1. CLOCK & TELEMETRY INITIALIZATION ---
function updateClock() {
    const now = new Date();
    hudClock.textContent = now.toLocaleTimeString();
}
setInterval(updateClock, 1000);
updateClock();

async function fetchTelemetry() {
    try {
        const res = await fetch("/api/status");
        if (res.ok) {
            const data = await res.json();
            if (data.stats) {
                cpuVal.textContent = data.stats.cpu_percent;
                ramVal.textContent = data.stats.ram_percent;
            }
            if (data.config) {
                backendVal.textContent = data.config.ai_backend ? data.config.ai_backend.toUpperCase() : "ONLINE";
                if (data.config.default_city) {
                    locVal.textContent = `${data.config.default_city.toUpperCase()}, IN`;
                }
            }
        }
    } catch (err) {
        // Silent catch for demo/offline viewing
    }
}
setInterval(fetchTelemetry, 3000);
fetchTelemetry();

// --- 2. HOLOGRAPHIC STATUS CHANGER ---
function setJarvisState(state) {
    arcReactor.classList.remove("listening", "speaking");
    statusDot.classList.remove("active", "speaking");

    if (state === "LISTENING") {
        statusText.textContent = "LISTENING FOR COMMAND...";
        reactorState.textContent = "// LISTENING //";
        arcReactor.classList.add("listening");
        statusDot.classList.add("active");
    } else if (state === "SPEAKING") {
        statusText.textContent = "TRANSMITTING VOICE OUTPUT";
        reactorState.textContent = "// VOCALIZING //";
        arcReactor.classList.add("speaking");
        statusDot.classList.add("speaking");
    } else if (state === "PROCESSING") {
        statusText.textContent = "NEURAL COMPUTATION...";
        reactorState.textContent = "// PROCESSING //";
        statusDot.classList.add("active");
    } else {
        statusText.textContent = "SYSTEM STANDBY";
        reactorState.textContent = "AWAITING VOICE INPUT";
    }
}

// --- 3. TRANSCRIPT & MESSAGING ---
function addMessage(sender, text, isUser = false) {
    const div = document.createElement("div");
    div.className = isUser ? "message user-msg" : "message jarvis-msg";
    
    const senderSpan = document.createElement("span");
    senderSpan.className = "sender";
    senderSpan.textContent = isUser ? "YOU:" : "J.A.R.V.I.S:";

    const p = document.createElement("p");
    p.textContent = text;

    div.appendChild(senderSpan);
    div.appendChild(p);
    chatLog.appendChild(div);
    chatLog.scrollTop = chatLog.scrollHeight;
}

function clearTranscript() {
    chatLog.innerHTML = "";
    addMessage("J.A.R.V.I.S", "Transcript cleared. Standby for new instructions, Sir.");
}

// --- 4. COMMAND SENDER & SERVER API ---
async function sendCommand(commandText) {
    if (!commandText || !commandText.trim()) return;
    const cleanCmd = commandText.trim();

    addMessage("YOU", cleanCmd, true);
    setJarvisState("PROCESSING");

    try {
        const response = await fetch("/api/command", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ command: cleanCmd })
        });

        if (response.ok) {
            const data = await response.json();
            const reply = data.reply || "Command executed.";
            addMessage("J.A.R.V.I.S", reply, false);
            speakBrowserTTS(reply);
        } else {
            const errReply = "An error occurred while transmitting to JARVIS server.";
            addMessage("J.A.R.V.I.S", errReply, false);
            speakBrowserTTS(errReply);
        }
    } catch (err) {
        // Fallback demo response if server offline
        const localReply = getLocalFallbackResponse(cleanCmd);
        addMessage("J.A.R.V.I.S", localReply, false);
        speakBrowserTTS(localReply);
    }
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendInput();
    }
}

function sendInput() {
    const text = commandInput.value;
    if (text.trim()) {
        sendCommand(text);
        commandInput.value = "";
    }
}

// --- 5. BROWSER SPEECH SYNTHESIS (TTS) ---
function speakBrowserTTS(text) {
    if (!browserTtsToggle.checked || !("speechSynthesis" in window)) {
        setJarvisState("STANDBY");
        return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.05;
    utterance.pitch = 0.95;

    // Try finding a British or deep male English voice
    const voices = window.speechSynthesis.getVoices();
    const preferredVoice = voices.find(v => v.lang.includes("en-GB") || v.name.includes("Daniel") || v.name.includes("Male")) || voices[0];
    if (preferredVoice) {
        utterance.voice = preferredVoice;
    }

    utterance.onstart = () => {
        setJarvisState("SPEAKING");
    };

    utterance.onend = () => {
        setJarvisState("STANDBY");
    };

    utterance.onerror = () => {
        setJarvisState("STANDBY");
    };

    window.speechSynthesis.speak(utterance);
}

// --- 6. BROWSER SPEECH RECOGNITION (MIC) ---
function toggleVoiceRecognition() {
    if (isListening) {
        stopVoiceRecognition();
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        alert("Web Speech API is not supported in this browser. Please use Google Chrome or Microsoft Edge.");
        return;
    }

    speechRecognizer = new SpeechRecognition();
    speechRecognizer.lang = "en-IN";
    speechRecognizer.continuous = false;
    speechRecognizer.interimResults = false;

    speechRecognizer.onstart = () => {
        isListening = true;
        micBtn.classList.add("active");
        micBtn.innerHTML = `<span class="mic-icon">🔴</span> LISTENING... SPEAK NOW`;
        setJarvisState("LISTENING");
    };

    speechRecognizer.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        sendCommand(transcript);
    };

    speechRecognizer.onerror = (event) => {
        console.error("Speech Recognition Error:", event.error);
        stopVoiceRecognition();
    };

    speechRecognizer.onend = () => {
        stopVoiceRecognition();
    };

    speechRecognizer.start();
}

function stopVoiceRecognition() {
    isListening = false;
    if (speechRecognizer) {
        try { speechRecognizer.stop(); } catch (e) {}
    }
    micBtn.classList.remove("active");
    micBtn.innerHTML = `<span class="mic-icon">🎤</span> ACTIVATE VOICE (HEY JARVIS)`;
    setJarvisState("STANDBY");
}

// --- 7. LOCAL DEMO FALLBACK (if backend API server not running) ---
function getLocalFallbackResponse(cmd) {
    const q = cmd.toLowerCase();
    if (q.includes("who are you") || q.includes("your name")) {
        return "I am JARVIS, Just A Rather Very Intelligent System. Your holographic interface is operational, Sir.";
    }
    if (q.includes("time") || q.includes("kitne baje")) {
        return `The current time is ${new Date().toLocaleTimeString()}, Sir.`;
    }
    if (q.includes("date") || q.includes("today")) {
        return `Today is ${new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}, Sir.`;
    }
    if (q.includes("joke") || q.includes("chutkula")) {
        return "Why do programmers prefer dark mode? Because light attracts bugs, Sir!";
    }
    if (q.includes("weather") || q.includes("mausam")) {
        return "The weather report in Asansol shows pleasant conditions with 68% humidity.";
    }
    return `I received command '${cmd}'. Connect the Python backend server (server.py) for live system automation and LLM intelligence!`;
}
