# LocalMind 🧠

A local-first AI assistant that lives in your taskbar — built for organizations where data never leaves the machine.

## Why I built this

During my PS-1 internship at Airports Authority of India (AAI), Guwahati, I noticed employees manually retyping content between systems because they couldn't use cloud AI tools on confidential government files. LocalMind solves that — all processing happens on your local hardware, zero internet required.

## Features (V1)
- Taskbar tray icon — always accessible
- Chat with a local LLM (Llama 3.1 8B via Ollama)
- No data sent to cloud, ever
- Password protection (coming soon)
- Screen capture + OCR (coming soon)
- Document Q&A via RAG (coming soon)

## Tech Stack
- Python, Tkinter, pystray
- Ollama (local LLM runner)
- Llama 3.1 8B
- LangChain + ChromaDB (upcoming)

## Setup
1. Install [Ollama](https://ollama.com) and run `ollama pull llama3.1`
2. Clone this repo
3. Create venv and install dependencies: `pip install -r requirements.txt`
4. Run `python app.py`

## Roadmap
- [ ] Screen capture + OCR pipeline
- [ ] Document RAG (PDF/DOCX Q&A)
- [ ] Password protection
- [ ] Hotkey to open from anywhere
- [ ] Package as `.exe`

---
Built during PS-1 @ AAI Guwahati | BITS Pilani