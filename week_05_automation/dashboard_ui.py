import tkinter as tk
from tkinter import ttk

class RTLSAutomationDashboard:
    def __init__(self, window_title="RuView RTLS Hub (Week 5)"):
        self.root = tk.Tk()
        self.root.title(window_title)
        self.root.geometry("450x300")
        self.root.configure(bg="#121212")
        
        # Style Definitions
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", background="#121212", foreground="#FFFFFF", font=("Segoe UI", 11))
        
        # Setup Interactive Visual Labels (Migrated to standard tk for clean background manipulation)
        self.title_lbl = tk.Label(self.root, text="RTLS Automation Node", bg="#121212", fg="#00FF66", font=("Segoe UI", 16, "bold"))
        self.title_lbl.pack(pady=15)
        
        self.state_lbl = tk.Label(self.root, text="SYSTEM STATE: PRESENT", bg="#1e1e1e", fg="#FFFFFF", font=("Segoe UI", 12, "bold"), width=30, height=2)
        self.state_lbl.pack(pady=10)
        
        self.metrics_lbl = tk.Label(self.root, text="Live Noise Variance: 0.00\nDynamic Timeout: 5.00s", bg="#121212", fg="#AAAAAA", font=("Segoe UI", 10))
        self.metrics_lbl.pack(pady=15)

    def update_display(self, current_state, live_variance, current_timeout):
        """Updates the interactive graphical interface elements cleanly."""
        self.state_lbl.config(text=f"SYSTEM STATE: {current_state}")
        
        # Shift color vectors based on deterministic states
        if current_state == "PRESENT":
            self.state_lbl.config(bg="#1b4d3e", fg="#00FF66")
        elif current_state == "UNSTABLE":
            self.state_lbl.config(bg="#6e4710", fg="#FFCC00")
        else:
            self.state_lbl.config(bg="#4d1b1b", fg="#FF3333")
            
        self.metrics_lbl.config(text=f"Live Noise Variance: {live_variance:.2f}\nDynamic Timeout: {current_timeout:.2f}s")
        
        # CRITICAL FIX: Resolved method name translation crash
        self.root.update_idletasks()
        self.root.update()