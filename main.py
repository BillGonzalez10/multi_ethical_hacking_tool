import tkinter as tk
from tkinter import ttk
import random

from hash_cracker import open_hash_cracker_window
from phishing import open_phishing_window
from recon_window import open_recon_window
from brute_force import open_bruteforce_window
from keylogger import open_keylogger_window
from sniffer import open_sniffer_window

# Root GUI setup
root = tk.Tk()
root.title("Multi_Tool")
root.geometry("600x650")
root.configure(bg="#001f00")  # Terminal dark green background

# ASCII banner splash (blood‑dripping style)
ascii_text = """
@@@@@@@    @@@@@@   @@@@@@@@@@   @@@  @@@  @@@       @@@  @@@   @@@@@@   @@@  @@@ 
@@@@@@@@  @@@@@@@@  @@@@@@@@@@@  @@@  @@@  @@@       @@@  @@@  @@@@@@@   @@@  @@@ 
@@!  @@@  @@!  @@@  @@! @@! @@!  @@!  @@@  @@!       @@!  @@@  !@@       @@!  !@@ 
!@!  @!@  !@!  @!@  !@! !@! !@!  !@!  @!@  !@!       !@!  @!@  !@!       !@!  @!! 
@!@!!@!   @!@  !@!  @!! !!@ @!@  @!@  !@!  @!!       @!@  !@!  !!@@!!     !@@!@!  
!!@!@!    !@!  !!!  !@!   ! !@!  !@!  !!!  !!!       !@!  !!!   !!@!!!     @!!!   
!!: :!!   !!:  !!!  !!:     !!:  !!:  !!!  !!:       !!:  !!!       !:!   !: :!!  
:!:  !:!  :!:  !:!  :!:     :!:  :!:  !:!   :!:      :!:  !:!      !:!   :!:  !:! 
::   :::  ::::: ::  :::     ::   ::::: ::   :: ::::  ::::: ::  :::: ::    ::  ::: 
 :   : :   : :  :    :      :     : :  :   : :: : :   : :  :   :: : :     :   ::  

               ⚔ Cybersecurity/EthicalHacking ToolKit ⚔
                        *  By Bill Gonzalez *
"""

ascii_label = tk.Label(root, text=ascii_text, fg="#33FF00", bg="#001f00", font=("Courier", 8), justify="left")
ascii_label.pack(pady=10)

# Flickering Title Label
title_label = tk.Label(root, text=">>> CYBERSECURITY TOOLKIT <<<", font=("Courier", 16, "bold"), fg="#33FF00", bg="#001f00")
title_label.pack(pady=5)

def flicker():
    if random.choice([True, False]):
        title_label.config(fg="#001f00")  # flicker off (invisible)
    else:
        title_label.config(fg="#33FF00")  # flicker on (green)
    root.after(120, flicker)  # flicker every 120ms

flicker()  # start the flicker loop

# Instructions label
tk.Label(root, text="Select a module to begin hacking:", fg="#33FF00", bg="#001f00", font=("Courier", 11)).pack(pady=5)

# Button styling
button_style = {
    "width": 25,
    "bg": "#003300",
    "fg": "#33FF00",
    "font": ("Courier", 12, "bold"),
    "activebackground": "#004d00",
    "activeforeground": "#99ff99"
}

# Tool Buttons
tk.Button(root, text="Recon and Network Scan", command=open_recon_window, **button_style).pack(pady=6)
tk.Button(root, text="Brute Force Attack", command=open_bruteforce_window, **button_style).pack(pady=6)
tk.Button(root, text="Hash Cracker", command=open_hash_cracker_window, **button_style).pack(pady=6)
tk.Button(root, text="Keylogger", command=open_keylogger_window, **button_style).pack(pady=6)
tk.Button(root, text="Packet Sniffer", command=open_sniffer_window, **button_style).pack(pady=6)
tk.Button(root, text="Phishing Page Simulator", command=open_phishing_window, **button_style).pack(pady=6)

root.mainloop()
