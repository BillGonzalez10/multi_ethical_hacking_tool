
import random
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading
from utils import export_to_txt, browse_file

def crack_hash(hash_value, wordlist_path, update_progress=None):
    try:
        with open(wordlist_path, "r", encoding="latin-1") as file:
            lines = file.readlines()
            total = len(lines)

        for idx, word in enumerate(lines):
            word = word.strip()
            if hashlib.md5(word.encode()).hexdigest() == hash_value:
                return f"[+] Match found: password: {word} | hash: {hash_value}"
            if update_progress:
                progress = int(((idx + 1) / total) * 100)
                update_progress(progress)

    except Exception as e:
        return f"Error: {e}"

    return "[-] No match found."

def open_hash_cracker_window():
    hash_cracker_window = tk.Toplevel()
    hash_cracker_window.title("Alien Terminal - Hash Cracker")
    hash_cracker_window.geometry("1024x768")
    hash_cracker_window.configure(bg="#000800")
    hash_cracker_window.resizable(False, False)

    canvas = tk.Canvas(hash_cracker_window, bg="#000800", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Scanlines
    for y in range(0, 768, 4):
        canvas.create_line(0, y, 1024, y, fill="#002200")

    # Title with flicker
    title_label = tk.Label(
        hash_cracker_window,
        text=">> HASH CRACKER MODULE <<",
        font=("Courier New", 16, "bold"),
        fg="#33FF00",
        bg="#000800"
    )
    title_label.place(x=320, y=30)

    def flicker_title():
        title_label.config(fg=random.choice(["#33FF00", "#000800"]))
        hash_cracker_window.after(150, flicker_title)

    flicker_title()

    label_style = {"font": ("Courier", 12), "fg": "#33FF00", "bg": "#000800"}
    entry_style = {"font": ("Courier", 12), "fg": "#33FF00", "bg": "#001100", "insertbackground": "#33FF00"}
    button_style = {"width": 15, "bg": "#001100", "fg": "#33FF00", "font": ("Courier", 11), "relief": "flat"}

    # Hash input
    tk.Label(hash_cracker_window, text="MD5 Hash:", **label_style).place(x=150, y=100)
    hash_entry = tk.Entry(hash_cracker_window, width=60, **entry_style)
    hash_entry.place(x=280, y=100)

    # Wordlist input
    tk.Label(hash_cracker_window, text="Wordlist File:", **label_style).place(x=150, y=140)
    wordlist_entry = tk.Entry(hash_cracker_window, width=50, **entry_style)
    wordlist_entry.place(x=280, y=140)
    tk.Button(hash_cracker_window, text="Browse", command=lambda: browse_file(wordlist_entry), **button_style).place(x=750, y=137)

    # Progress Bar
    style = ttk.Style()
    style.theme_use("default")
    style.configure("green.Horizontal.TProgressbar",
                    troughcolor="#000800",
                    background="#33FF00",
                    bordercolor="#000800",
                    lightcolor="#33FF00",
                    darkcolor="#33FF00")
    progress_bar = ttk.Progressbar(hash_cracker_window, orient="horizontal", length=500, mode="determinate", style="green.Horizontal.TProgressbar")
    progress_bar.place(x=260, y=190)

    # Output box
    output_box = scrolledtext.ScrolledText(
        hash_cracker_window, height=20, width=85, state=tk.DISABLED,
        bg="#000000", fg="#33FF00", insertbackground="#33FF00",
        font=("Courier", 10), borderwidth=0,
        highlightbackground="#33FF00", highlightcolor="#33FF00"
    )
    output_box.place(x=130, y=230)

    def update_progress(value):
        progress_bar["value"] = value
        progress_bar.update()

    def start_cracking():
        hash_value = hash_entry.get()
        wordlist_path = wordlist_entry.get()

        if not hash_value or not wordlist_path:
            messagebox.showwarning("Input Required", "Please enter a hash and select a wordlist.")
            return

        output_box.config(state=tk.NORMAL)
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, "Cracking hash...\n")
        output_box.config(state=tk.DISABLED)

        def crack():
            result = crack_hash(hash_value, wordlist_path, update_progress)
            output_box.config(state=tk.NORMAL)
            output_box.insert(tk.END, result)
            output_box.config(state=tk.DISABLED)
            progress_bar["value"] = 100

        threading.Thread(target=crack, daemon=True).start()

    # Buttons
    tk.Button(
        hash_cracker_window,
        text="Start Cracking",
        command=start_cracking,
        bg="#001100", fg="#33FF00",
        activebackground="#003300", activeforeground="#99ff99",
        font=("Courier New", 12, "bold"), width=22, relief="flat"
    ).place(x=400, y=660)

    tk.Button(
        hash_cracker_window,
        text="Export to TXT",
        command=lambda: export_to_txt(output_box, parent=hash_cracker_window),
        bg="#001100", fg="#33FF00",
        activebackground="#003300", activeforeground="#99ff99",
        font=("Courier New", 12, "bold"), width=22, relief="flat"
    ).place(x=400, y=700)
