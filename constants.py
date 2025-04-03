
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BRANCH_WIDTH = 480
BRANCH_HEIGHT = 60
BIRD_SIZE = 80
MAX_BIRDS_PER_BRANCH = 4
COLORS = [
    (255, 0, 0),    # Red
    (255, 255, 255),# Brown
    (0, 255, 0),    # Green
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Purple
    (0, 255, 255),  # Cyan
    (255, 128, 0),  # Orange
    (128, 0, 255),  # Indigo
    (255, 0, 128),  # Pink
    (0, 255, 128),  # Teal
    (128, 255, 0)   # Lime
]
num_colors = 4

ALGORITHM_TIMEOUT = 60  # seconds
ALGORITHM_SLEEP = 0.5  # seconds

import pygame
clock = pygame.time.Clock()
delta_time = clock.tick(60) / 1000.0  # Convert milliseconds to seconds

bird_height = 40
bird_width = 40

# TODO: Rename this file to globals.py
