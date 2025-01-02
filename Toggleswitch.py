import tkinter as tk
from tkinter import Canvas
import random


class DayNightToggle:
    def __init__(self, master):
        self.master = master
        self.master.title("Day/Night Toggle Switch")

        self.canvas = Canvas(master, width=400, height=200, bg="white")
        self.canvas.pack()

        self.is_day = True
        self.draw_day()

        self.toggle_button = tk.Button(master, text="Toggle", command=self.toggle)
        self.toggle_button.pack(pady=10)

    def draw_day(self):
        self.canvas.delete("all")
        # Draw the sun
        self.canvas.create_oval(150, 30, 250, 130, fill="yellow", outline="yellow")
        self.canvas.create_text(200, 160, text="Day", font=("Arial", 24), fill="black")

    def draw_night(self):
        self.canvas.delete("all")
        # Draw the night sky
        self.canvas.create_rectangle(0, 0, 400, 200, fill="black")
        # Draw stars
        for _ in range(20):
            x = random.randint(0, 400)
            y = random.randint(0, 200)
            self.canvas.create_oval(x, y, x + 5, y + 5, fill="white", outline="white")
        self.canvas.create_text(200, 160, text="Night", font=("Arial", 24), fill="white")

    def toggle(self):
        if self.is_day:
            self.animate_to_night()
        else:
            self.animate_to_day()

    def animate_to_night(self):
        for i in range(10):
            self.canvas.after(i * 100, self.draw_night)
            self.canvas.update()
        self.is_day = False

    def animate_to_day(self):
        for i in range(10):
            self.canvas.after(i * 100, self.draw_day)
            self.canvas.update()
        self.is_day = True


if __name__ == "__main__":
    root = tk.Tk()
    toggle = DayNightToggle(root)
    root.mainloop()