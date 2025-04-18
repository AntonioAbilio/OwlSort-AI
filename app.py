import ctypes
import pygame
import sys
from windows.state_manager import StateManager
from windows.mainmenu import MainMenu
from global_vars import Globals

# Initialize pygame
pygame.init()

# Set screen width and height in global_vars
Globals.SCREEN_WIDTH = pygame.display.Info().current_w
Globals.SCREEN_HEIGHT = pygame.display.Info().current_h

# Set up the icon
programIcon = pygame.image.load('assets/static_cucu.png')
pygame.display.set_icon(programIcon)

# Set up the screen
screen = pygame.display.set_mode((Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Bird Sort 2: Color Puzzle")
clock = pygame.time.Clock()
Globals.DELTA_TIME = clock.tick(60) / 1000.0

def main():
    mainMenu = MainMenu()
    stateManager = StateManager(mainMenu)
        
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN: # Check if ESC was pressed
                if event.key == pygame.K_ESCAPE:
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