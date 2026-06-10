import pystray
from PIL import Image, ImageDraw
import threading
import tkinter as tk
from tkinter import scrolledtext
import ollama

def create_icon():
    img = Image.new('RGB', (64, 64), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    draw.ellipse([8, 8, 56, 56], fill=(0, 120, 212))
    return img

def ask_llm(prompt):
    response = ollama.chat(model='llama3.1', messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']

def open_window():
    win = tk.Tk()
    win.title("LocalMind")
    win.geometry("600x400")
    win.configure(bg="#1e1e1e")

    output = scrolledtext.ScrolledText(win, wrap=tk.WORD, bg="#2d2d2d", fg="white", font=("Consolas", 11))
    output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    entry = tk.Entry(win, bg="#3d3d3d", fg="white", font=("Consolas", 11))
    entry.pack(fill=tk.X, padx=10, pady=(0, 10))

    def submit(event=None):
        prompt = entry.get()
        if not prompt:
            return
        entry.delete(0, tk.END)
        output.insert(tk.END, f"You: {prompt}\n")
        output.insert(tk.END, "LocalMind: thinking...\n")
        win.update()

        def get_response():
            reply = ask_llm(prompt)
            output.insert(tk.END, f"LocalMind: {reply}\n\n")
            output.see(tk.END)

        threading.Thread(target=get_response, daemon=True).start()

    entry.bind("<Return>", submit)
    win.mainloop()

def on_open(icon, item):
    threading.Thread(target=open_window, daemon=True).start()

def on_quit(icon, item):
    icon.stop()

def run_tray():
    icon = pystray.Icon(
        "LocalMind",
        create_icon(),
        "LocalMind",
        menu=pystray.Menu(
            pystray.MenuItem("Open", on_open),
            pystray.MenuItem("Quit", on_quit)
        )
    )
    icon.run()

if __name__ == "__main__":
    print("LocalMind starting...")
    run_tray()