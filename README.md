# LocalMind 🧠

A local-first AI assistant that lives in your taskbar — built for organizations where data never leaves the machine.

## Why I built this

During my PS-1 internship at Airports Authority of India (AAI), Guwahati, I noticed employees manually retyping content between systems because they couldn't use cloud AI on confidential government files. LocalMind solves that — all processing happens on your local hardware, zero internet required.

## Features (V1)
- Taskbar tray icon — always accessible
- Global hotkey `Ctrl+Shift+Space` to open from anywhere
- Chat with a local LLM (Llama 3.1 8B via Ollama)
- Screen region selector — draw a box around any text on screen
- OCR pipeline with DPI fix and image preprocessing
- Actions: Summarize, Explain, Key Points on any screen content
- Document RAG — load any PDF and ask questions about it
- Everything runs locally, zero cloud, zero API calls

## Tech Stack
- Python, Tkinter, pystray
- Ollama (local LLM runner) + Llama 3.1 8B
- pytesseract + Pillow (OCR)
- sentence-transformers (local embeddings)
- ChromaDB (local vector database)
- LangChain (document loading)
- PyInstaller (packaging, coming soon)

## Setup
1. Install [Ollama](https://ollama.com) and run `ollama pull llama3.1`
2. Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
3. Clone this repo
4. Create venv: `python -m venv venv && venv\Scripts\activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Run: `python app.py`

## Usage
- Press `Ctrl+Shift+Space` or click the tray icon to open
- **Chat** — type anything in the input box
- **Scan screen** — click Summarize/Explain/Key Points, draw a box around any text
- **Document Q&A** — click Load Document, select a PDF, ask questions in chat

## Roadmap
- [x] Local LLM chat
- [x] Taskbar tray icon
- [x] Global hotkey
- [x] Screen region OCR
- [x] Document RAG (PDF Q&A)
- [ ] Password protection
- [ ] DOCX support
- [ ] Conversation history
- [ ] Package as `.exe`
- [ ] Demo video

---
Built during PS-1 @ Airports Authority of India, Guwahati | BITS Pilani 2028