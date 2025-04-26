
import tkinter as tk
import random
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import time
from brute import run_hydra
from utils import export_to_txt

def gui_bruteforce():
    target = brute_target_entry.get()
    userlist = userlist_entry.get()
    passlist = passlist_entry.get()

    if not target or not userlist or not passlist:
        messagebox.showwarning("Input Required", "Please fill all fields.")
        return

    output_box.config(state=tk.NORMAL)
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, "Running Hydra brute force attack...\n")
    output_box.config(state=tk.DISABLED)

    progress_bar["value"] = 0
    progress_bar.update()

    try:
        with open(passlist, "r") as f:
            total_lines = sum(1 for _ in f)
    except Exception as e:
        messagebox.showerror("Error", f"Could not read password list: {e}")
        return

    def run():
        for i in range(1, total_lines + 1):
            time.sleep(0.1)
            progress = int((i / total_lines) * 100)
            progress_bar["value"] = progress
            progress_bar.update()

        result = run_hydra(target, userlist, passlist)
        output_box.config(state=tk.NORMAL)
        output_box.insert(tk.END, result)
        output_box.config(state=tk.DISABLED)
        progress_bar["value"] = 100

    threading.Thread(target=run, daemon=True).start()

def browse_file(entry_field):
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, filepath)

def open_bruteforce_window():
    global brute_target_entry, userlist_entry, passlist_entry, output_box, progress_bar

    brute_window = tk.Toplevel()
    brute_window.title("Alien Terminal - Hydra Brute Force")
    brute_window.geometry("1024x768")
    brute_window.configure(bg="#000800")
    brute_window.resizable(False, False)

    canvas = tk.Canvas(brute_window, bg="#000800", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Scanlines
    for y in range(0, 768, 4):
        canvas.create_line(0, y, 1024, y, fill="#002200")

    # Title label
    title_label = tk.Label(
        brute_window,
        text=">> HYDRA BRUTE FORCE MODULE <<",
        font=("Courier New", 16, "bold"),
        fg="#33FF00",
        bg="#000800"
    )
    title_label.place(x=300, y=30)

    def flicker_title():
        title_label.config(fg=random.choice(["#33FF00", "#000800"]))
        brute_window.after(150, flicker_title)

    flicker_title()

    entry_style = {"font": ("Courier", 12), "fg": "#33FF00", "bg": "#001100", "insertbackground": "#33FF00"}
    label_style = {"font": ("Courier", 12), "fg": "#33FF00", "bg": "#000800"}
    button_style = {"width": 15, "bg": "#001100", "fg": "#33FF00", "font": ("Courier", 11), "relief": "flat"}

    # Target
    tk.Label(brute_window, text="Target URL:", **label_style).place(x=130, y=100)
    brute_target_entry = tk.Entry(brute_window, width=60, **entry_style)
    brute_target_entry.place(x=270, y=100)

    # Userlist
    tk.Label(brute_window, text="Userlist:", **label_style).place(x=130, y=140)
    userlist_entry = tk.Entry(brute_window, width=50, **entry_style)
    userlist_entry.place(x=270, y=140)
    tk.Button(brute_window, text="Browse", command=lambda: browse_file(userlist_entry), **button_style).place(x=750, y=137)

    # Passlist
    tk.Label(brute_window, text="Passlist:", **label_style).place(x=130, y=180)
    passlist_entry = tk.Entry(brute_window, width=50, **entry_style)
    passlist_entry.place(x=270, y=180)
    tk.Button(brute_window, text="Browse", command=lambda: browse_file(passlist_entry), **button_style).place(x=750, y=177)

    # Progress Bar
    style = ttk.Style()
    style.theme_use("default")
    style.configure("green.Horizontal.TProgressbar",
                    troughcolor="#000800",
                    background="#33FF00",
                    bordercolor="#000800",
                    lightcolor="#33FF00",
                    darkcolor="#33FF00")
    progress_bar = ttk.Progressbar(brute_window, orient="horizontal", length=500, mode="determinate", style="green.Horizontal.TProgressbar")
    progress_bar.place(x=260, y=230)

    # Output Box
    output_box = scrolledtext.ScrolledText(
        brute_window, height=20, width=85, state=tk.DISABLED,
        bg="#000000", fg="#33FF00", insertbackground="#33FF00",
        font=("Courier", 10), borderwidth=0,
        highlightbackground="#33FF00", highlightcolor="#33FF00"
    )
    output_box.place(x=130, y=270)

    # Buttons
    tk.Button(
        brute_window,
        text="Launch Attack",
        command=gui_bruteforce,
        bg="#001100", fg="#33FF00",
        activebackground="#003300", activeforeground="#99ff99",
        font=("Courier New", 12, "bold"), width=22, relief="flat"
    ).place(x=400, y=660)

    tk.Button(
        brute_window,
        text="Export Output",
        command=lambda: export_to_txt(output_box, parent=brute_window),
        bg="#001100", fg="#33FF00",
        activebackground="#003300", activeforeground="#99ff99",
        font=("Courier New", 12, "bold"), width=22, relief="flat"
    ).place(x=400, y=700)
