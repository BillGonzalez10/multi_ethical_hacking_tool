import time
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import threading
import random
from utils import export_to_txt
from recon_tools import nmap_scan as external_nmap_scan, scan_vulnerabilities, whois_lookup, find_subdomains


def open_recon_window():
    recon_window = tk.Toplevel()
    recon_window.title("Alien Terminal - Recon Tools")
    recon_window.geometry("1024x768")
    recon_window.configure(bg="#000800")
    recon_window.resizable(False, False)

    canvas = tk.Canvas(recon_window, bg="#000800", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Scanlines
    for y in range(0, 768, 4):
        canvas.create_line(0, y, 1024, y, fill="#002200")

    # Flickering title
    title_label = tk.Label(
        recon_window,
        text=">> NETWORK RECONNAISSANCE MODULE <<",
        font=("Courier New", 16, "bold"),
        fg="#33FF00",
        bg="#000800"
    )
    title_label.place(x=270, y=30)

    def flicker_title():
        title_label.config(fg=random.choice(["#33FF00", "#000800"]))
        recon_window.after(150, flicker_title)

    flicker_title()

    # Input label & entry
    input_label = tk.Label(
        recon_window,
        text="Enter Target (IP or Domain) / URL with vuln param:",
        font=("Courier", 12),
        fg="#33FF00",
        bg="#000800"
    )
    input_label.place(x=270, y=100)

    recon_target_entry = tk.Entry(
        recon_window,
        width=50,
        font=("Courier", 12),
        fg="#33FF00",
        bg="#001100",
        insertbackground="#33FF00",
        relief="flat"
    )
    recon_target_entry.place(x=270, y=130)

    # Output box
    output_box = scrolledtext.ScrolledText(
        recon_window,
        height=20,
        width=85,
        state=tk.DISABLED,
        font=("Courier New", 11),
        fg="#33FF00",
        bg="#000000",
        insertbackground="#33FF00",
        borderwidth=0,
        highlightbackground="#33FF00",
        highlightcolor="#33FF00"
    )
    output_box.place(x=130, y=180)

    # Progress bar
    progress_bar = ttk.Progressbar(
        recon_window,
        orient="horizontal",
        length=500,
        mode="indeterminate"
    )
    progress_bar.place(x=260, y=620)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("green.Horizontal.TProgressbar",
                    troughcolor="#000800",
                    background="#33FF00",
                    bordercolor="#000800",
                    lightcolor="#33FF00",
                    darkcolor="#33FF00")
    progress_bar.config(style="green.Horizontal.TProgressbar")

    def flash_red():
        def do_flash():
            for _ in range(4):
                output_box.config(bg="#FF1C1C")
                time.sleep(0.2)
                output_box.config(bg="#000000")
                time.sleep(0.2)
        threading.Thread(target=do_flash, daemon=True).start()

    def run_with_progress(tool_func, target, highlight_vulns=False):
        progress_bar.start()

        def task():
            result = tool_func(target)
            progress_bar.stop()

            output_box.config(state=tk.NORMAL)
            output_box.delete(1.0, tk.END)

            output_box.tag_config("vuln", foreground="#FF3131")
            output_box.tag_config("fix", foreground="#33FF00")

            found_vuln = False
            for line in result.splitlines():
                if any(keyword in line.lower() for keyword in [
                    "not present", "missing", "retrieved", "unencrypted", "wildcard", "error"
                ]):
                    output_box.insert(tk.END, line + "\n", "vuln")
                    found_vuln = True
                elif "Fix:" in line:
                    output_box.insert(tk.END, line + "\n", "fix")
                    found_vuln = True
                else:
                    output_box.insert(tk.END, line + "\n")

            output_box.config(state=tk.DISABLED)

            if highlight_vulns and found_vuln:
                flash_red()

        threading.Thread(target=task, daemon=True).start()

    def gui_nmap_scan():
        target = recon_target_entry.get()
        if not target:
            messagebox.showwarning("Input Required", "Please enter a target.")
            return
        run_with_progress(external_nmap_scan, target)

    def gui_vuln_scan():
        target = recon_target_entry.get()
        if not target:
            messagebox.showwarning("Input Required", "Please enter a target.")
            return
        run_with_progress(scan_vulnerabilities, target, highlight_vulns=True)

    def gui_whois():
        target = recon_target_entry.get()
        if not target:
            messagebox.showwarning("Input Required", "Please enter a target.")
            return
        run_with_progress(whois_lookup, target)

    def gui_subfinder():
        target = recon_target_entry.get()
        if not target:
            messagebox.showwarning("Input Required", "Please enter a target.")
            return
        run_with_progress(find_subdomains, target)

    # Button style
    btn_style = {
        "bg": "#001100",
        "fg": "#33FF00",
        "activebackground": "#003300",
        "activeforeground": "#99ff99",
        "font": ("Courier New", 12, "bold"),
        "width": 22,
        "relief": "flat"
    }

    # Buttons
    tk.Button(recon_window, text="Nmap Scan", command=gui_nmap_scan, **btn_style).place(x=130, y=660)
    tk.Button(recon_window, text="Vulnerability Scan", command=gui_vuln_scan, **btn_style).place(x=330, y=660)
    tk.Button(recon_window, text="Whois Lookup", command=gui_whois, **btn_style).place(x=530, y=660)
    tk.Button(recon_window, text="Subdomain Finder", command=gui_subfinder, **btn_style).place(x=730, y=660)

    # Export Button
    tk.Button(
        recon_window,
        text="Export to TXT",
        command=lambda: export_to_txt(output_box, parent=recon_window),
        **btn_style
    ).place(x=420, y=700)
