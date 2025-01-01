import tkinter as tk

class HoverCard:
    def __init__(self, parent):
        self.parent = parent
        self.hover_card = tk.Frame(
            parent,
            bg="#ffb142",
            highlightbackground="#ff793f",
            highlightthickness=3,
            bd=5
        )
        self.hover_paused = False
        self.click_count = 0

        # Add card content
        self.card_title = tk.Label(
            self.hover_card,
            text="I LOVE YOU",
            bg="#ffb142",
            fg="white",
            font=("Arial", 14, "bold"),
        )
        self.card_title.pack(pady=(10, 5))

        self.card_description = tk.Label(
            self.hover_card,
            text="A SMALL GIFT FOR YOU",
            bg="#ffb142",
            fg="#2c2c54",
            font=("Arial", 10),
            wraplength=200,
            justify="left"
        )
        self.card_description.pack(pady=(0, 10), padx=10)

        self.card_button = tk.Button(
            self.hover_card,
            text="Click Me",
            bg="#ff793f",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            activebackground="#ff5252",
            activeforeground="white",
            command=self.on_button_click
        )
        self.card_button.pack(pady=(0, 10))

    def on_hover(self, event):
        if not self.hover_paused:
            self.animate_hover_card(event.x_root + 10, event.y_root + 10)
            self.hover_card.lift()

    def off_hover(self, event):
        if not self.hover_paused:
            self.hover_card.place_forget()

    def animate_hover_card(self, target_x, target_y):
        current_x, current_y = self.hover_card.winfo_x(), self.hover_card.winfo_y()
        delta_x = (target_x - current_x) // 5  # Smooth step size
        delta_y = (target_y - current_y) // 5

        # Move closer to the target position
        if abs(delta_x) > 1 or abs(delta_y) > 1:
            self.hover_card.place(x=current_x + delta_x, y=current_y + delta_y)
            self.parent.after(16, self.animate_hover_card, target_x, target_y)  # 60 FPS
        else:
            self.hover_card.place(x=target_x, y=target_y)  # Final position

    def toggle_hover_card(self, event):
        self.click_count += 1

        if self.click_count == 1:  # Pause the card on the first click
            self.hover_paused = True
        elif self.click_count == 2:  # Hide the card on the second click
            self.hover_card.place_forget()
            self.hover_paused = False
            self.click_count = 0  # Reset click count

    def on_button_click(self):
        self.click_count = 0  # Reset click count
        self.hover_paused = False  # Reset hover state
        self.hover_card.place_forget()  # Hide the card momentarily

        # Show a thank-you message
        message_label = tk.Label(self.parent, text="Thank you for clicking! 😊", font=("Arial", 12), fg="#34ace0")
        message_label.place(x=200, y=300)
        self.parent.after(1500, message_label.destroy)  # Remove message after 1.5 seconds

# Main application window
def main():
    root = tk.Tk()
    root.geometry("500x400")
    root.title("Hover Card Example")

    # Create hover card instance
    hover_card = HoverCard(root)

    label = tk.Label(root, text="TOUCH HERE", font=("Arial", 14), bg="#34ace0", fg="white")
    label.pack(pady=50)

    label.bind("<Enter>", hover_card.on_hover)
    label.bind("<Motion>", hover_card.on_hover)
    label.bind("<Leave>", hover_card.off_hover)
    hover_card.hover_card.bind("<Button-1>", hover_card.toggle_hover_card)  # Bind card click event

    root.mainloop()

if __name__ == "__main__":
    main()
