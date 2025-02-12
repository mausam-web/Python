import tkinter as tk
import random
import pygame
from tkinter import messagebox, filedialog

# Try to import Pillow for better image handling (PNG/JPEG, resizing, etc.)
try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

# Initialize pygame mixer for sound effects
pygame.mixer.init()

# Load sound effects (ensure these files exist in your project folder)
eat_sound = pygame.mixer.Sound("eat.mp3")  # Sound when the snake eats food
game_over_sound = pygame.mixer.Sound("gameover.mp3")  # Sound when the game ends

# Global game variables
direction = (20, 0)  # Initial direction (right)
scores = []  # To store history of scores
paused = False  # Game pause state
current_theme = "Dark"  # Default theme

# Predefined theme configurations (color-based themes)
themes = {
    "Dark": {"bg": "black", "snake": "lime", "food": "red"},
    "Light": {"bg": "white", "snake": "blue", "food": "orange"},
    "Nature": {"bg": "#2E8B57", "snake": "#FFD700", "food": "#8B0000"}
}

# --- Set Up the Main Window with a Fixed Size ---
root = tk.Tk()
root.title("Snake Game with Attractive Boundary Walls & Sound")

GRID_SIZE = 20
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
WALL_THICKNESS = GRID_SIZE  # Wall thickness (adjustable)

root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT,
                   bg=themes[current_theme]["bg"])
canvas.pack()


# --- Main Game Functions ---

def start_game(level):
    global direction, paused, snake, food, score
    direction = (20, 0)  # Reset direction

    # Start the snake near the center of the screen
    start_x = SCREEN_WIDTH // 2
    start_y = SCREEN_HEIGHT // 2
    snake = [
        (start_x, start_y),
        (start_x - GRID_SIZE, start_y),
        (start_x - 2 * GRID_SIZE, start_y)
    ]
    food = spawn_food(snake)  # Ensure food doesn't spawn on the snake or wall
    score = 0
    speed = {"easy": 200, "medium": 150, "hard": 100}[level]
    paused = False  # Reset pause state

    # Set canvas background (if using a custom image theme, the image will be drawn later)
    if "bg_image" in themes[current_theme]:
        canvas.configure(bg="white")
    else:
        canvas.configure(bg=themes[current_theme]["bg"])

    def move_snake():
        if paused:
            root.after(speed, move_snake)
            return

        global food, score
        head_x, head_y = snake[0]
        # Calculate the new head position (normal movement)
        new_head = (head_x + direction[0], head_y + direction[1])

        # Check if the snake hits the boundary wall:
        if (new_head[0] < WALL_THICKNESS or new_head[0] >= SCREEN_WIDTH - WALL_THICKNESS or
                new_head[1] < WALL_THICKNESS or new_head[1] >= SCREEN_HEIGHT - WALL_THICKNESS):
            scores.append(score)
            game_over_sound.play()  # Play game over sound
            show_game_over()
            return

        # Check for self-collision:
        if new_head in snake:
            scores.append(score)
            game_over_sound.play()  # Play game over sound
            show_game_over()
            return

        snake.insert(0, new_head)

        if new_head == food:
            score += 10
            eat_sound.play()  # Play eating sound effect
            food = spawn_food(snake)
        else:
            snake.pop()

        draw_game()
        root.after(speed, move_snake)

    def draw_game():
        canvas.delete("all")
        # Draw background image if a custom theme is active.
        if "bg_image" in themes[current_theme]:
            canvas.create_image(0, 0, anchor="nw", image=themes[current_theme]["bg_image"])

        # Draw boundary walls (as four filled rectangles)
        # Top wall
        canvas.create_rectangle(0, 0, SCREEN_WIDTH, WALL_THICKNESS, fill="brown", outline="brown")
        # Bottom wall
        canvas.create_rectangle(0, SCREEN_HEIGHT - WALL_THICKNESS, SCREEN_WIDTH, SCREEN_HEIGHT, fill="brown",
                                outline="brown")
        # Left wall
        canvas.create_rectangle(0, 0, WALL_THICKNESS, SCREEN_HEIGHT, fill="brown", outline="brown")
        # Right wall
        canvas.create_rectangle(SCREEN_WIDTH - WALL_THICKNESS, 0, SCREEN_WIDTH, SCREEN_HEIGHT, fill="brown",
                                outline="brown")

        # Draw the snake (using ovals for a smoother appearance)
        for segment in snake:
            x, y = segment
            canvas.create_oval(x, y, x + GRID_SIZE, y + GRID_SIZE,
                               fill=themes[current_theme]["snake"],
                               outline="")

        # Draw the food as a circle.
        canvas.create_oval(food[0], food[1], food[0] + GRID_SIZE, food[1] + GRID_SIZE,
                           fill=themes[current_theme]["food"],
                           outline="")

        # Display the current score.
        canvas.create_text(50, 10, text=f"Score: {score}",
                           fill="white", font=("Arial", 14), anchor="nw")

    move_snake()


def spawn_food(snake):
    while True:
        x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        # Ensure food spawns within the safe area (inside the walls)
        if ((x, y) not in snake and
            WALL_THICKNESS <= x < SCREEN_WIDTH - WALL_THICKNESS and
            WALL_THICKNESS <= y < SCREEN_HEIGHT - WALL_THICKNESS):
            return (x, y)



def change_direction(new_direction):
    global direction
    # Prevent the snake from reversing directly.
    if (new_direction[0] * -1, new_direction[1] * -1) != direction:
        direction = new_direction


def toggle_pause(event=None):
    global paused
    paused = not paused


def show_game_over():
    canvas.delete("all")
    canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                       text="GAME OVER", fill="red",
                       font=("Arial", 30, "bold"))
    canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                       text=f"Your Score: {scores[-1]}",
                       fill="white", font=("Arial", 20))
    restart_button = tk.Button(root, text="Restart", command=show_level_menu)
    canvas.create_window(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, window=restart_button)


def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Score History")
    history_window.geometry("300x400")
    tk.Label(history_window, text="Score History", font=("Arial", 16)).pack(pady=10)
    if not scores:
        tk.Label(history_window, text="No games played yet!", font=("Arial", 12)).pack()
    else:
        for i, score in enumerate(scores, 1):
            tk.Label(history_window, text=f"Game {i}: {score}").pack()
    tk.Button(history_window, text="Close", command=history_window.destroy).pack(pady=10)


def show_level_menu():
    menu_window = tk.Toplevel(root)
    menu_window.title("Select Level")
    menu_window.geometry("300x300")
    tk.Label(menu_window, text="Select Difficulty", font=("Arial", 16)).pack(pady=10)
    tk.Button(menu_window, text="Easy",
              command=lambda: [menu_window.destroy(), start_game("easy")]).pack(pady=5)
    tk.Button(menu_window, text="Medium",
              command=lambda: [menu_window.destroy(), start_game("medium")]).pack(pady=5)
    tk.Button(menu_window, text="Hard",
              command=lambda: [menu_window.destroy(), start_game("hard")]).pack(pady=5)
    tk.Button(menu_window, text="Change Theme",
              command=lambda: [menu_window.destroy(), show_theme_menu()]).pack(pady=5)
    tk.Button(menu_window, text="View History",
              command=lambda: [menu_window.destroy(), show_history()]).pack(pady=5)


# --- Theme Menu & Custom Theme Loading ---

def show_theme_menu():
    theme_window = tk.Toplevel(root)
    theme_window.title("Select Theme")
    theme_window.geometry("300x300")
    tk.Label(theme_window, text="Select Theme", font=("Arial", 16)).pack(pady=10)

    def set_theme(theme):
        global current_theme
        current_theme = theme
        theme_window.destroy()
        show_level_menu()  # Return to level selection after choosing a theme

    # List predefined (color-based) themes.
    for theme in themes.keys():
        if theme != "Custom":  # Exclude the custom theme if already set
            tk.Button(theme_window, text=theme,
                      command=lambda t=theme: set_theme(t)).pack(pady=5)
    # Option to load a custom theme from a file.
    tk.Button(theme_window, text="Custom Theme", command=load_custom_theme).pack(pady=5)


def load_custom_theme():
    file_path = filedialog.askopenfilename(
        title="Select Background Image",
        filetypes=(("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*"))
    )
    if file_path:
        global current_theme
        try:
            if Image is not None:
                img = Image.open(file_path)
                img = img.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.ANTIALIAS)
                custom_bg = ImageTk.PhotoImage(img)
            else:
                custom_bg = tk.PhotoImage(file=file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image file: {e}")
            return
        # Create a new custom theme using the loaded image.
        themes["Custom"] = {"bg_image": custom_bg, "snake": "cyan", "food": "magenta"}
        current_theme = "Custom"
        show_level_menu()


# --- Main Start Button & Key Bindings ---

start_button = tk.Button(root, text="Start Game", command=show_level_menu)
start_button.pack(pady=10)

root.bind("<Up>", lambda event: change_direction((0, -GRID_SIZE)))
root.bind("<Down>", lambda event: change_direction((0, GRID_SIZE)))
root.bind("<Left>", lambda event: change_direction((-GRID_SIZE, 0)))
root.bind("<Right>", lambda event: change_direction((GRID_SIZE, 0)))
root.bind("<space>", toggle_pause)

root.mainloop()
