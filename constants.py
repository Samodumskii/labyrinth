import pygame

# Display settings
WIDTH, HEIGHT = 802, 802
RES = WIDTH, HEIGHT
TILE = 100
# Size of a labyrinth
COLS, ROWS = WIDTH // TILE, HEIGHT // TILE
THICKNESS = 1
# Game time
TIME = 30
# Control buttons
BUTTONS = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}
# Color dictionary for door, key
COLOR_DICT = {0: "Red", 1: "Green", 2: "Blue"}
MAX_COUNT = len(COLOR_DICT)-1
# Speed character
SPEED = 5
FPS = 60
# Path to background picture
BACKGROUND = 'img/background.jpeg'