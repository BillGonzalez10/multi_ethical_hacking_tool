import tkinter as tk
from tkinter import scrolledtext
import threading
import random
import subprocess
from utils import monitor_credentials, export_to_txt

def open_phishing_window():
    phishing_window = tk.Toplevel()
    phishing_window.title("Phishing Simulator")
    phishing_window.geometry("1024x768")
    phishing_window.configure(bg="#000800")
    phishing_window.resizable(False, False)

    canvas = tk.Canvas(phishing_window, bg="#000800", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Scanlines for CRT effect
    for y in range(0, 768, 4):
        canvas.create_line(0, y, 1024, y, fill="#002200")

    # Flickering title
    title_label = tk.Label(phishing_window, text=">> PHISHING PAGE SIMULATOR <<",
                           font=("Courier New", 18, "bold"),
                           fg="#33FF00", bg="#000800")
    title_label.place(x=300, y=30)

    def flicker_title():
        title_label.config(fg=random.choice(["#33FF00", "#000800"]))
        phishing_window.after(150, flicker_title)

    flicker_title()

    # Output terminal box
    output_box = scrolledtext.ScrolledText(
        phishing_window,
        height=22,
        width=90,
        state=tk.DISABLED,
        bg="#000800",
        fg="#33FF00",
        insertbackground="#33FF00",
        font=("Courier New", 12),
        borderwidth=0,
        highlightbackground="#33FF00",
        highlightcolor="#33FF00"
    )
    output_box.place(x=80, y=100)

    # Footer Instructions (Alien style)
    # canvas.create_text(80, 740, anchor="nw",
    #                   text="[↑↓]: navigate | [←→]: scroll | [Q]: exit",
    #                   font=("Courier New", 10), fill="#33FF00")

    # Server launcher
    def start_server():
        try:
            subprocess.Popen(["python3", "login_server.py"])
        except Exception as e:
            output_box.config(state=tk.NORMAL)
            output_box.insert(tk.END, f"[!] Error: {e}\n")
            output_box.yview(tk.END)
            output_box.config(state=tk.DISABLED)

    # Monitor login credentials
    def start_monitor():
        threading.Thread(target=monitor_credentials, args=(output_box,), daemon=True).start()

    # Button aesthetic
    button_style = {
        "bg": "#001100",
        "fg": "#33FF00",
        "activebackground": "#003300",
        "activeforeground": "#99ff99",
        "font": ("Courier New", 12, "bold"),
        "width": 22,
        "relief": "flat"
    }

    tk.Button(phishing_window, text="Start Login Server", command=start_server, **button_style).place(x=180, y=660)
    tk.Button(phishing_window, text="Start Monitoring", command=start_monitor, **button_style).place(x=430, y=660)
    tk.Button(phishing_window, text="Export to TXT",
              command=lambda: export_to_txt(output_box, parent=phishing_window), **button_style).place(x=680, y=660)
