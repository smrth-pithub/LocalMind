import bcrypt
import json
import os
import tkinter as tk
from tkinter import messagebox

CONFIG_PATH = "localmind_config.json"

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f)

def is_password_set():
    config = load_config()
    return "password_hash" in config

def set_password(password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    config = load_config()
    config["password_hash"] = hashed
    save_config(config)

def verify_password(password):
    config = load_config()
    if "password_hash" not in config:
        return False
    return bcrypt.checkpw(password.encode(), config["password_hash"].encode())

def show_set_password():
    """First launch - set a new password"""
    result = [False]
    
    win = tk.Tk()
    win.title("LocalMind — Set Password")
    win.geometry("350x200")
    win.configure(bg="#1e1e1e")
    win.resizable(False, False)

    tk.Label(win, text="Welcome to LocalMind", bg="#1e1e1e", fg="white",
             font=("Consolas", 13, "bold")).pack(pady=(20, 5))
    tk.Label(win, text="Set a password to protect your data", bg="#1e1e1e",
             fg="#888888", font=("Consolas", 10)).pack(pady=(0, 15))

    entry = tk.Entry(win, show="*", bg="#3d3d3d", fg="white",
                     font=("Consolas", 11), width=25)
    entry.pack(pady=(0, 10))

    error_label = tk.Label(win, text="", bg="#1e1e1e", fg="#ff4444", font=("Consolas", 9))
    error_label.pack()

    def confirm():
        password = entry.get()
        if len(password) < 4:
            error_label.config(text="Password must be at least 4 characters")
            return
        set_password(password)
        result[0] = True
        win.destroy()

    tk.Button(win, text="Set Password", command=confirm,
              bg="#0078d4", fg="white", font=("Consolas", 10),
              bd=0, padx=15, pady=6).pack(pady=(5, 0))

    entry.bind("<Return>", lambda e: confirm())
    entry.focus()
    win.mainloop()
    return result[0]

def show_login():
    """Subsequent launches - verify password"""
    result = [False]

    win = tk.Tk()
    win.title("LocalMind — Login")
    win.geometry("350x200")
    win.configure(bg="#1e1e1e")
    win.resizable(False, False)

    tk.Label(win, text="LocalMind", bg="#1e1e1e", fg="white",
             font=("Consolas", 13, "bold")).pack(pady=(20, 5))
    tk.Label(win, text="Enter your password to continue", bg="#1e1e1e",
             fg="#888888", font=("Consolas", 10)).pack(pady=(0, 15))

    entry = tk.Entry(win, show="*", bg="#3d3d3d", fg="white",
                     font=("Consolas", 11), width=25)
    entry.pack(pady=(0, 10))

    error_label = tk.Label(win, text="", bg="#1e1e1e", fg="#ff4444", font=("Consolas", 9))
    error_label.pack()

    def confirm():
        if verify_password(entry.get()):
            result[0] = True
            win.destroy()
        else:
            error_label.config(text="Incorrect password")
            entry.delete(0, tk.END)

    tk.Button(win, text="Unlock", command=confirm,
              bg="#0078d4", fg="white", font=("Consolas", 10),
              bd=0, padx=15, pady=6).pack(pady=(5, 0))

    entry.bind("<Return>", lambda e: confirm())
    entry.focus()
    win.mainloop()
    return result[0]

def authenticate():
    """Main auth flow — call this on startup"""
    if not is_password_set():
        return show_set_password()
    else:
        return show_login()