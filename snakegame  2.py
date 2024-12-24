import pygame
import time
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
GAME_WIDTH, GAME_HEIGHT = WIDTH, HEIGHT - 100
SCOREBOARD_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Snake and food colors
SNAKE_COLOR = (34, 139, 34)  # Forest Green
FOOD_COLOR = (255, 99, 71)   # Tomato

# Block size for snake and food
BLOCK_SIZE = 20

# Initial frame rate and speed
INITIAL_SPEED = 0.1
LEVEL_THRESHOLD = 50

# File for storing scores
SCORE_FILE = "scores.txt"

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Snake Game")

# Clock
clock = pygame.time.Clock()

# Font for messages
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def message(msg, color, x, y):
    msg_surface = font_style.render(msg, True, color)
    screen.blit(msg_surface, [x, y])

def your_score(score, level, best_score):
    value = score_font.render(f"Score: {score}  Level: {level}  Best Score: {best_score}", True, BLUE)
    screen.blit(value, [0, 0])

def draw_scoreboard(score, level, best_score):
    # Draw a scoreboard at the top
    pygame.draw.rect(screen, BLACK, [0, 0, WIDTH, SCOREBOARD_HEIGHT])
    your_score(score, level, best_score)

def save_score(score):
    with open(SCORE_FILE, "a") as file:
        file.write(f"{score}\n")

def get_best_score():
    if not os.path.exists(SCORE_FILE):
        return 0
    with open(SCORE_FILE, "r") as file:
        scores = [int(line.strip()) for line in file if line.strip().isdigit()]
    return max(scores) if scores else 0

def display_history():
    if not os.path.exists(SCORE_FILE):
        scores = []
    else:
        with open(SCORE_FILE, "r") as file:
            scores = [line.strip() for line in file if line.strip().isdigit()]

    history_screen = True
    while history_screen:
        screen.fill(BLACK)
        message("Score History:", GREEN, WIDTH // 4, HEIGHT // 6)
        for i, score in enumerate(scores[-10:]):
            message(f"{i + 1}. {score}", WHITE, WIDTH // 4, HEIGHT // 4 + i * 30)
        message("Press B to go back to the main menu.", YELLOW, WIDTH // 4, HEIGHT - 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    main_menu()

def main_menu():
    menu = True
    while menu:
        screen.fill(BLACK)
        message("Welcome to the Snake Game!", GREEN, WIDTH // 4, HEIGHT // 4)
        message("Press S to Start, Q to Quit", WHITE, WIDTH // 4, HEIGHT // 3)
        message("Press H for Help", YELLOW, WIDTH // 4, HEIGHT // 2.5)
        message("Press V to View Score History", BLUE, WIDTH // 4, HEIGHT // 2.2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game_loop()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_h:
                    help_menu()
                if event.key == pygame.K_v:
                    display_history()

def help_menu():
    help_screen = True
    while help_screen:
        screen.fill(BLACK)
        message("Instructions:", GREEN, WIDTH // 4, HEIGHT // 4)
        message("1. Use arrow keys to move the snake.", WHITE, WIDTH // 4, HEIGHT // 3)
        message("2. Eat food to grow and increase score.", WHITE, WIDTH // 4, HEIGHT // 2.5)
        message("3. Avoid hitting walls or yourself.", WHITE, WIDTH // 4, HEIGHT // 2.2)
        message("Press B to go back to the main menu.", YELLOW, WIDTH // 4, HEIGHT // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    main_menu()

def game_loop():
    game_over = False
    game_close = False

    # Initial position of the snake
    x1, y1 = WIDTH // 2, HEIGHT // 2
    x1_change, y1_change = 0, 0
    snake_list = []
    length_of_snake = 1

    # Food position
    foodx = round(random.randrange(0, GAME_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    foody = round(random.randrange(SCOREBOARD_HEIGHT, GAME_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    level = 1
    score = 0
    current_speed = INITIAL_SPEED
    best_score = get_best_score()

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            message("You lost! Press C to Play Again or Q to Quit", RED, WIDTH // 6, HEIGHT // 3)
            your_score(score, level, best_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        save_score(score)
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        save_score(score)
                        main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_score(score)
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        if x1 >= GAME_WIDTH or x1 < 0 or y1 >= GAME_HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)

        # Draw food
        pygame.draw.rect(screen, FOOD_COLOR, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        # Update snake body
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        for block in snake_list:
            pygame.draw.rect(screen, SNAKE_COLOR, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

        your_score(score, level, best_score)
        draw_scoreboard(score, level, best_score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, GAME_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            foody = round(random.randrange(SCOREBOARD_HEIGHT, GAME_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            length_of_snake += 1
            score += 10  # Increase score
            if score >= level * LEVEL_THRESHOLD:
                level += 1
                current_speed -= 0.01  # Increase difficulty

        time.sleep(current_speed)

    pygame.quit()

# Start game
main_menu()
