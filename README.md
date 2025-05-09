# 🧠 Voice Assistant with LiveKit & ESP32 LED Control (FREE)

A Basic Python-based voice assistant powered by [LiveKit Agents](https://github.com/livekit/agents), .to toggle led on or off

---

## ✨ Features

- 🎤 Real-time speech interaction
- 🧠 LLM integration using Google Gemini
- 🗣️ Deepgram for multilingual speech-to-text (STT)
- 🔊 Cartesia for text-to-speech (TTS)
- 🧘‍♂️ Noise cancellation and voice activity detection
- 💡 Voice-controlled LED via ESP32 and HTTP API
- 🧩 Modular design with extensible command support using `@function_tool`

---

## 🧪 Requirements

- Python 3.8+
- ESP32 Development Board
- A WiFi network for ESP32 + Python app to communicate

---

## ⚙️ Setup Instructions

### 🔧 1. Clone the Repo

```bash
git clone https://github.com/hulomjosuan21/voice-assistant
cd voice-assistant

python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

# Example .env
LIVEKIT_URL=your_livekit_url
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
GOOGLE_API_KEY=your_gemini_api_key
CARTESIA_API_KEY=your_cartesia_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key


### Run the the agent to console via voice or text prompt
```base
python agent.py console
```


### and upload the .ino file to the esp32