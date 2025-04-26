import os
import time
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

CREDENTIALS_FILE = '/home/kali/Desktop/cyber_ethical_tool/credentials.txt'
def export_to_txt(output_box, parent=None):
    text = output_box.get(1.0, tk.END).strip()
    if not text:
        messagebox.showwarning("Empty Output", "There is no content to export.", parent=parent)
        return

    file_path = filedialog.asksaveasfilename(
        parent=parent, 
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if file_path:
        with open(file_path, "w") as file:
            file.write(text)
        messagebox.showinfo("Success", f"Output saved to {file_path}", parent=parent)


def browse_file(entry_field):
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, filepath)


# Function to run subprocess or wrapped command and update output box
def run_command(command, output_box):
    try:
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        output_box.config(state=tk.NORMAL)
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, process.stdout)
        output_box.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to execute command: {e}")

# GUI-based wrapper for external functions
def run_tool_func(tool_func, target, output_box):
    try:
        output_box.config(state=tk.NORMAL)
        output_box.delete(1.0, tk.END)

        result = tool_func(target)

        # Apply tag styling
        output_box.tag_config("vuln", foreground="#FF3131")    # Red for vulns
        output_box.tag_config("fix", foreground="#33FF00")     # Green for fixes

        for line in result.splitlines():
            if any(keyword in line.lower() for keyword in ["not present", "missing", "retrieved", "unencrypted", "wildcard", "error"]):
                output_box.insert(tk.END, line + "\n", "vuln")
            elif "Fix:" in line:
                output_box.insert(tk.END, line + "\n", "fix")
            else:
                output_box.insert(tk.END, line + "\n")

        output_box.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", f"Tool failed: {e}")

def monitor_credentials(output_box):
    last_size = 0
    while True:
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, 'r') as f:
                content = f.read()
                if len(content) > last_size:  # Only update if new data is added
                    output_box.config(state=tk.NORMAL)
                    output_box.delete(1.0, tk.END)
                    output_box.insert(tk.END, content)
                    output_box.config(state=tk.DISABLED)
                    last_size = len(content)  # Update last known file size
        time.sleep(1)
