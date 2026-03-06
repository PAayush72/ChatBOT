# Chatbot

A lightweight Python-based conversational agent built for experimentation with local LLMs and web-socket interfaces. Ideal for showcasing full-stack AI integration and custom prompt engineering.

## ⭐ Key Features

- **Modular architecture**  
  - `core/` – chat engine, memory management, prompt templates and LLM wrapper  
  - `api/` – HTTP & WebSocket endpoints (`chat.py`, `ws_chat.py`) for real-time interaction  
  - `db/` – SQLite models & session persistence  
  - `models/` – stores the `mistral-7b-instruct-v0.2` GGUF weights for offline inference

- **Web client demo**  
  - `websocket_chat.html` demonstrates live chat via WebSockets  
  - `main.py` runs a minimal server to serve the page and API

- **Local inference support**  
  - Custom `llm.py` handles loading and querying a local Mistral‑7B model  
  - Designed to work offline with quantized GGUF files

- **Persistent memory & context**  
  - `memory.py` and `fact_store.py` let the bot remember past exchanges  
  - `session.py` in `db/` keeps conversation state across requests

- **Extensible prompt system**  
  - `prompt.py` centralises prompt templates; easily adjusted for new behaviors

## 📁 Directory Structure

```
main.py
websocket_chat.html
api/
  chat.py
  ws_chat.py
core/
  chat_engine.py
  fact_store.py
  llm.py
  memory.py
  prompt.py
db/
  init_db.py
  models.py
  session.py
models/
  mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

## 🚀 Getting Started

1. Clone the repo.
2. Set up a Python environment and install dependencies.
3. Place your GGUF model in `models/`.
4. Run `main.py` to start the server.
5. Open `websocket_chat.html` in a browser to interact.

## 💡 Why It’s Portfolio‑Worthy

- Demonstrates full‑stack development: backend API, real‑time WebSocket UI, and machine‑learning integration.
- Shows ability to work with cutting‑edge open‑source LLMs offline.
- Designed with clean separation of concerns and easy extensibility.

Feel free to adapt this description for your GitHub README or portfolio site—add screenshots or usage examples to make it even more compelling!
