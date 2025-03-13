import pygame
import sys
from windows.state_manager import StateManager
from windows.mainmenu import MainMenu
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)

# Initialize pygame
pygame.init()

# Set up the screen
#screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED) # TODO: This might be better for scaling (Test with a non 4k display)
#ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Enable DPI scaling # TODO: This might be better for scaling (Test with a non 4k display)

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