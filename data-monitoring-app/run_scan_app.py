import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

def run_monitor():
    try:
        # Adjust the path if needed
        monitor_path = os.path.join(os.path.dirname(__file__), 'data_monitoring_app', 'monitor.py')
        subprocess.run([sys.executable, monitor_path], check=True)
        messagebox.showinfo("Scan Complete", "monitor.py executed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run monitor.py:\n{e}")

root = tk.Tk()
root.title("Run Data Monitor Scan")
root.geometry("300x150")

run_button = tk.Button(root, text="Run Scan", command=run_monitor, font=("Arial", 14), width=15)
run_button.pack(pady=40)

root.mainloop()