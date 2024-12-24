import tkinter as tk
from tkinter import messagebox
import random

class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock-Paper-Scissors")
        self.root.geometry("300x200")

        self.player_score = 0
        self.computer_score = 0

        self.player_score_label = tk.Label(self.root, text="Player Score: 0", font=("Arial", 12))
        self.player_score_label.pack()

        self.computer_score_label = tk.Label(self.root, text="Computer Score: 0", font=("Arial", 12))
        self.computer_score_label.pack()

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack()

        self.rock_button = tk.Button(self.root, text="Rock", command=lambda: self.play("Rock"))
        self.rock_button.pack(side=tk.LEFT)

        self.paper_button = tk.Button(self.root, text="Paper", command=lambda: self.play("Paper"))
        self.paper_button.pack(side=tk.LEFT)

        self.scissors_button = tk.Button(self.root, text="Scissors", command=lambda: self.play("Scissors"))
        self.scissors_button.pack(side=tk.LEFT)

    def play(self, player_choice):
        choices = ["Rock", "Paper", "Scissors"]
        computer_choice = random.choice(choices)

        if player_choice == computer_choice:
            result = "It's a tie!"
        elif (player_choice == "Rock" and computer_choice == "Scissors") or \
             (player_choice == "Paper" and computer_choice == "Rock") or \
             (player_choice == "Scissors" and computer_choice == "Paper"):
            result = "Player wins!"
            self.player_score += 1
        else:
            result = "Computer wins!"
            self.computer_score += 1

        self.result_label['text'] = f"Player: {player_choice}, Computer: {computer_choice}, {result}"
        self.player_score_label['text'] = f"Player Score: {self.player_score}"
        self.computer_score_label['text'] = f"Computer Score: {self.computer_score}"

        if self.player_score == 3:
            messagebox.showinfo("Game Over", "Player wins the game!")
            self.root.quit()
        elif self.computer_score == 3:
            messagebox.showinfo("Game Over", "Computer wins the game!")
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissors(root)
    root.mainloop()