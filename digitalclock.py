import time
import tkinter as tk

class DigitalClock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Digital Clock")
        self.date_label = tk.Label(self.root, font=('Helvetica', 24), fg='blue')
        self.date_label.pack()
        self.time_label = tk.Label(self.root, font=('Helvetica', 48), fg='green')
        self.time_label.pack()
        self.update_clock()
        self.root.mainloop()

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%A, %B %d, %Y")
        self.time_label.config(text=current_time)
        self.date_label.config(text=current_date)
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    clock = DigitalClock()