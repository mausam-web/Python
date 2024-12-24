import tkinter as tk
from tkinter import messagebox

class Chatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot")
        self.root.geometry("400x400")


        self.frame_input = tk.Frame(self.root)
        self.frame_input.pack(fill="x")

        self.frame_output = tk.Frame(self.root)
        self.frame_output.pack(fill="both", expand=True)


        self.input_entry = tk.Entry(self.frame_input, width=40)
        self.input_entry.pack(side="left")

        # Create send button
        self.send_button = tk.Button(self.frame_input, text="Send", command=self.send_message)
        self.send_button.pack(side="left")

        # Create output text box
        self.output_text = tk.Text(self.frame_output, width=40, height=10)
        self.output_text.pack(fill="both", expand=True)

        # Initialize chatbot responses
        self.responses = {
            "hello": "Hi! How can I help you today?",
            "hi": "Hello! What's on your mind?",
            "how are you": "I'm doing great, thanks! How about you?",
            "what is your name": "I'm Chatbot, nice to meet you!",
            "default": "I didn't understand that. Can you please rephrase?"
        }

    def send_message(self):
        user_input = self.input_entry.get()
        self.input_entry.delete(0, "end")

        response = self.get_response(user_input)
        self.output_text.insert("end", f"User: {user_input}\n")
        self.output_text.insert("end", f"Chatbot: {response}\n\n")

    def get_response(self, user_input):
        user_input = user_input.lower()
        for key in self.responses:
            if key in user_input:
                return self.responses[key]
        return self.responses["default"]

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    chatbot = Chatbot(root)
    chatbot.run()
