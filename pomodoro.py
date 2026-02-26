import tkinter as tk
from tkinter import messagebox
import time
import json
import os
from datetime import datetime

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Focus - Pomodoro Timer")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.WORK_MIN = 25
        self.BREAK_MIN = 5
        self.seconds = self.WORK_MIN * 60
        self.is_running = False
        self.is_work = True
        self.pomodoros_today = 0

        self.load_stats()

        # UI Elements
        self.label = tk.Label(root, text="25:00", font=("Helvetica", 48), fg="black")
        self.label.pack(pady=30)

        self.status = tk.Label(root, text="Work Time", font=("Helvetica", 16))
        self.status.pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)

        self.start_btn = tk.Button(btn_frame, text="Start", command=self.start, width=10)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.pause_btn = tk.Button(btn_frame, text="Pause", command=self.pause, state="disabled", width=10)
        self.pause_btn.grid(row=0, column=1, padx=10)

        reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset, width=10)
        reset_btn.grid(row=0, column=2, padx=10)

        self.stats_label = tk.Label(root, text=f"Pomodoros today: {self.pomodoros_today}", font=("Helvetica", 12))
        self.stats_label.pack(pady=10)

        self.update_display()  # initial display

    def load_stats(self):
        today = datetime.now().strftime("%Y-%m-%d")
        if os.path.exists("stats.json"):
            with open("stats.json", "r") as f:
                data = json.load(f)
                if today in data:
                    self.pomodoros_today = data[today]

    def save_stats(self):
        today = datetime.now().strftime("%Y-%m-%d")
        data = {}
        if os.path.exists("stats.json"):
            with open("stats.json", "r") as f:
                data = json.load(f)
        data[today] = self.pomodoros_today
        with open("stats.json", "w") as f:
            json.dump(data, f, indent=4)

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.start_btn.config(state="disabled")
            self.pause_btn.config(state="normal")
            self.countdown()

    def pause(self):
        self.is_running = False
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")

    def reset(self):
        self.pause()
        self.is_work = True
        self.seconds = self.WORK_MIN * 60
        self.update_display()
        self.status.config(text="Work Time")

    def countdown(self):
        if self.is_running and self.seconds > 0:
            self.seconds -= 1
            self.update_display()
            self.root.after(1000, self.countdown)
        elif self.seconds == 0:
            if self.is_work:
                self.pomodoros_today += 1
                self.stats_label.config(text=f"Pomodoros today: {self.pomodoros_today}")
                self.save_stats()
                messagebox.showinfo("Great job!", "Take a 5-minute break!")
                self.is_work = False
                self.seconds = self.BREAK_MIN * 60
                self.status.config(text="Break Time")
            else:
                messagebox.showinfo("Break over", "Back to work!")
                self.is_work = True
                self.seconds = self.WORK_MIN * 60
                self.status.config(text="Work Time")
            self.start()  # auto start next phase (or pause if you prefer)

    def update_display(self):
        mins = self.seconds // 60
        secs = self.seconds % 60
        self.label.config(text=f"{mins:02d}:{secs:02d}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()