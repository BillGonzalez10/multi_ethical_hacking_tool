
import tkinter as tk
from tkinter import scrolledtext

import random
from network_tools import toggle_sniffer, sniffing_active
from utils import export_to_txt

def open_sniffer_window():
    sniffer_window = tk.Toplevel()
    sniffer_window.title("Alien Terminal - Packet Sniffer")
    sniffer_window.geometry("1024x768")
    sniffer_window.configure(bg="#000800")
    sniffer_window.resizable(False, False)

    canvas = tk.Canvas(sniffer_window, bg="#000800", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Horizontal scanlines
    for y in range(0, 768, 4):
        canvas.create_line(0, y, 1024, y, fill="#002200")

    # ASCII Banner
    banner_text = """
    ██████╗  █████╗  ██████╗██╗  ██╗███████╗████████╗     ███████╗███╗   ██╗██╗███████╗███████╗██████╗ 
    ██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝╚══██╔══╝     ██╔════╝████╗  ██║██║██╔════╝██╔════╝██╔══██╗
    ██████╔╝███████║██║     █████╔╝ █████╗     ██║        █████╗  ██╔██╗ ██║██║█████╗  █████╗  ██║  ██║
    ██╔═══╝ ██╔══██║██║     ██╔═██╗ ██╔══╝     ██║        ██╔══╝  ██║╚██╗██║██║██╔══╝  ██╔══╝  ██║  ██║
    ██║     ██║  ██║╚██████╗██║  ██╗███████╗   ██║        ███████╗██║ ╚████║██║██║     ███████╗██████╔╝
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝        ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═════╝ 
    """
    tk.Label(
        sniffer_window, text=banner_text,
        font=("Courier New", 8),
        fg="#33FF00", bg="#000800", justify="left"
    ).place(x=30, y=10)

    # Title with flicker
    title_label = tk.Label(
        sniffer_window, text=">> PACKET SNIFFER MODULE <<",
        font=("Courier New", 14, "bold"),
        fg="#33FF00", bg="#000800"
    )
    title_label.place(x=360, y=130)

    def flicker_title():
        title_label.config(fg=random.choice(["#33FF00", "#000800"]))
        sniffer_window.after(150, flicker_title)

    flicker_title()

    # Output box
    output_box = scrolledtext.ScrolledText(
        sniffer_window, height=20, width=100, state=tk.DISABLED,
        bg="#000000", fg="#33FF00", insertbackground="#33FF00",
        font=("Courier", 10), borderwidth=0,
        highlightbackground="#33FF00", highlightcolor="#33FF00"
    )
    output_box.place(x=60, y=180)

    # Button style
    button_style = {
        "bg": "#001100",
        "fg": "#33FF00",
        "activebackground": "#003300",
        "activeforeground": "#99ff99",
        "font": ("Courier New", 12, "bold"),
        "width": 22,
        "relief": "flat"
    }

    # This function updates the button label after toggling
    def handle_toggle():
        toggle_sniffer(output_box)
        toggle_button.config(text="Stop Sniffer" if sniffing_active else "Start Sniffer")

    toggle_button = tk.Button(
        sniffer_window, text="Start Sniffer",
        command=handle_toggle,
        **button_style
    )
    toggle_button.place(x=400, y=620)

    tk.Button(
        sniffer_window, text="Export to TXT",
        command=lambda: export_to_txt(output_box, parent=sniffer_window),
        **button_style
    ).place(x=400, y=660)
