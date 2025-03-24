
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BRANCH_WIDTH = 480
BRANCH_HEIGHT = 60
BIRD_SIZE = 80
MAX_BIRDS_PER_BRANCH = 5
COLORS = [
    (255, 0, 0),    # Red
    (255, 255, 255),# Brown
    (0, 255, 0),    # Green
    (255, 255, 0),  # Yellow
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
