import pygame
import sys
from state_manager import State, StateManager
from mainmenu import MainMenu
from birdsort import GameState, Game
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)

# Initialize pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bird Sort 2: Color Puzzle")
clock = pygame.time.Clock()

def main():
    mainMenu = MainMenu()
    stateManager = StateManager(mainMenu)
    print("Game initialized. Press the hint button to test BFS algorithm.")
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                running = False
            stateManager.handle_event(event)
        
        stateManager.update()
        stateManager.draw(screen)
                
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()