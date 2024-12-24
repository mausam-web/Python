import tkinter as tk
from tkinter import ttk

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("400x300")

        # Create frames
        self.frame_tasks = ttk.Frame(self.root)
        self.frame_tasks.pack(fill="both", expand=True)

        self.frame_buttons = ttk.Frame(self.root)
        self.frame_buttons.pack(fill="x")

        # Create task list
        self.task_list = tk.Listbox(self.frame_tasks, width=40, height=10)
        self.task_list.pack(side="left", fill="both", expand=True)

        # Create scrollbar
        self.scrollbar = tk.Scrollbar(self.frame_tasks)
        self.scrollbar.pack(side="right", fill="y")
        self.task_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_list.yview)

        # Create entry field
        self.entry_task = tk.Entry(self.frame_buttons, width=30)
        self.entry_task.pack(side="left", fill="x", expand=True)

        # Create buttons
        self.button_add = ttk.Button(self.frame_buttons, text="Add Task", command=self.add_task)
        self.button_add.pack(side="left", fill="x", expand=True)

        self.button_done = ttk.Button(self.frame_buttons, text="Mark as Done", command=self.mark_done)
        self.button_done.pack(side="left", fill="x", expand=True)

        self.button_delete = ttk.Button(self.frame_buttons, text="Delete Task", command=self.delete_task)
        self.button_delete.pack(side="left", fill="x", expand=True)

        # Initialize task list
        self.tasks = []

    def add_task(self):
        task = self.entry_task.get()
        if task:
            self.tasks.append({"task": task, "done": False})
            self.task_list.insert("end", task)
            self.entry_task.delete(0, "end")

    def mark_done(self):
        selection = self.task_list.curselection()
        if selection:
            task_index = selection[0]
            self.tasks[task_index]["done"] = True
            self.task_list.delete(task_index)
            self.task_list.insert(task_index, f"{self.tasks[task_index]['task']} (Done)")

    def delete_task(self):
        selection = self.task_list.curselection()
        if selection:
            task_index = selection[0]
            del self.tasks[task_index]
            self.task_list.delete(task_index)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()