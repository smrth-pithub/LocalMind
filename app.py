import pystray
from PIL import Image, ImageDraw, ImageGrab
import threading
import tkinter as tk
from tkinter import scrolledtext, filedialog
import ollama
import pytesseract
import ctypes
import os
from rag import load_pdf, query_document

ctypes.windll.shcore.SetProcessDpiAwareness(2)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# --- OCR Region Selector ---
class RegionSelector:
    def __init__(self):
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.rect = None

    def select_region(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.configure(bg='black')
        self.root.attributes('-topmost', True)
        self.canvas = tk.Canvas(self.root, cursor='cross', bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind('<ButtonPress-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.root.mainloop()
        return self.capture_region()

    def on_press(self, event):
        self.start_x = self.root.winfo_pointerx()
        self.start_y = self.root.winfo_pointery()

    def on_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        cur_x = self.root.winfo_pointerx()
        cur_y = self.root.winfo_pointery()
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, cur_x, cur_y,
            outline='red', width=2
        )

    def on_release(self, event):
        self.end_x = self.root.winfo_pointerx()
        self.end_y = self.root.winfo_pointery()
        self.root.destroy()

    def capture_region(self):
        x1 = min(self.start_x, self.end_x)
        y1 = min(self.start_y, self.end_y)
        x2 = max(self.start_x, self.end_x)
        y2 = max(self.start_y, self.end_y)
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        screenshot = screenshot.convert('L')
        screenshot = screenshot.point(lambda x: 0 if x < 140 else 255)
        text = pytesseract.image_to_string(screenshot)
        return text

# --- LLM ---
def ask_llm(prompt):
    response = ollama.chat(model='llama3.1', messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']

# --- Main Window ---
def open_window():
    win = tk.Tk()
    win.title("LocalMind")
    win.geometry("700x550")
    win.configure(bg="#1e1e1e")

    # Output area
    output = scrolledtext.ScrolledText(win, wrap=tk.WORD, bg="#2d2d2d", fg="white", font=("Consolas", 11))
    output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Document state
    current_collection = [None]

    # Document bar
    doc_frame = tk.Frame(win, bg="#1e1e1e")
    doc_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

    doc_label = tk.Label(doc_frame, text="No document loaded", bg="#1e1e1e", fg="#888888", font=("Consolas", 10))
    doc_label.pack(side=tk.LEFT, padx=4)

    def load_document():
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not path:
            return
        output.insert(tk.END, f"[Loading document...]\n")
        win.update()

        def do_load():
            collection_name, pages = load_pdf(path)
            current_collection[0] = collection_name
            doc_label.config(text=f"📄 {os.path.basename(path)} ({pages} pages)", fg="#00cc66")
            output.insert(tk.END, f"[Document loaded: {pages} pages — ask questions about it in the chat]\n\n")
            output.see(tk.END)

        threading.Thread(target=do_load, daemon=True).start()

    tk.Button(doc_frame, text="Load Document", command=load_document,
        bg="#2d8a4e", fg="white", font=("Consolas", 10), bd=0, padx=10, pady=5).pack(side=tk.LEFT, padx=4)

    # Action buttons
    btn_frame = tk.Frame(win, bg="#1e1e1e")
    btn_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

    def scan_and_action(action):
        output.insert(tk.END, f"[Scanning screen...]\n")
        win.update()

        def run():
            selector = RegionSelector()
            text = selector.select_region()

            if not text.strip():
                output.insert(tk.END, "[No text found in selection]\n\n")
                return

            prompts = {
                "Summarize": f"Summarize the following text concisely:\n\n{text}",
                "Explain": f"Explain the following text in simple terms:\n\n{text}",
                "Key Points": f"Extract the key points from the following text as a bullet list:\n\n{text}",
            }

            output.insert(tk.END, f"[Extracted text]\n{text}\n\n")
            output.insert(tk.END, f"LocalMind ({action}): thinking...\n")
            win.update()

            reply = ask_llm(prompts[action])
            output.insert(tk.END, f"LocalMind: {reply}\n\n")
            output.see(tk.END)

        threading.Thread(target=run, daemon=True).start()

    btn_style = {"bg": "#0078d4", "fg": "white", "font": ("Consolas", 10), "bd": 0, "padx": 10, "pady": 5}

    tk.Button(btn_frame, text="Summarize", command=lambda: scan_and_action("Summarize"), **btn_style).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Explain", command=lambda: scan_and_action("Explain"), **btn_style).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Key Points", command=lambda: scan_and_action("Key Points"), **btn_style).pack(side=tk.LEFT, padx=4)

    # Chat input
    entry = tk.Entry(win, bg="#3d3d3d", fg="white", font=("Consolas", 11))
    entry.pack(fill=tk.X, padx=10, pady=(0, 10))
    entry.insert(0, "Ask anything or load a document above...")
    entry.bind("<FocusIn>", lambda e: entry.delete(0, tk.END))

    def submit(event=None):
        prompt = entry.get()
        if not prompt:
            return
        entry.delete(0, tk.END)
        output.insert(tk.END, f"You: {prompt}\n")
        output.insert(tk.END, "LocalMind: thinking...\n")
        win.update()

        def get_response():
            if current_collection[0]:
                reply = query_document(current_collection[0], prompt)
            else:
                reply = ask_llm(prompt)
            output.insert(tk.END, f"LocalMind: {reply}\n\n")
            output.see(tk.END)

        threading.Thread(target=get_response, daemon=True).start()

    entry.bind("<Return>", submit)
    win.mainloop()

# --- Tray ---
def create_icon():
    img = Image.new('RGB', (64, 64), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    draw.ellipse([8, 8, 56, 56], fill=(0, 120, 212))
    return img

def on_open(icon, item):
    threading.Thread(target=open_window, daemon=True).start()

def on_quit(icon, item):
    icon.stop()

def run_tray():

    print("Creating tray icon...")
    icon = pystray.Icon(
        "LocalMind",
        create_icon(),
        "LocalMind",
        menu=pystray.Menu(
            pystray.MenuItem("Open", on_open),
            pystray.MenuItem("Quit", on_quit)
        )
    )
    print("Running Tray...")
    icon.run()

    print("Tray stopped.")

def setup_hotkey():
    import keyboard
    keyboard.add_hotkey('ctrl+shift+space', lambda: threading.Thread(target=open_window, daemon=True).start())
    keyboard.wait()

if __name__ == "__main__":
    print("LocalMind starting...")
    print("Hotkey: Ctrl+Shift+Space to open")
    threading.Thread(target=setup_hotkey, daemon=True).start()
    run_tray()

#if __name__ == "__main__":
 #   print("LocalMind starting...")
  #  open_window()   