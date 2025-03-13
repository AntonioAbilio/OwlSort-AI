import pygame
import sys
from levels import import_manager
from windows.state_manager import State
from windows.choose_level import ChooseLevel
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)
from models.button import Button

class MainMenu(State) :
    def __init__(self):
        super().__init__()
        self.title = pygame.image.load("assets/title.png")
        self.upper_left_branch = pygame.image.load("assets/branch.png")
        self.cucu = pygame.image.load("assets/static_cucu.png")
        self.start_button = Button(SCREEN_WIDTH/4 - 200, SCREEN_HEIGHT/2 - 50, 180, 50, "Start", (200, 200, 255), (150, 150, 255))
        self.quit_button = Button(SCREEN_WIDTH/4 - 200, SCREEN_HEIGHT/2 - 50 + 188, 180, 50, "Quit", (200, 200, 255), (150, 150, 255))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if start button was clicked
            if self.start_button.is_clicked(mouse_pos):
                self.next_state = ChooseLevel()
                return
            
            # Check if quit button was clicked
            if self.quit_button.is_clicked(mouse_pos):
                pygame.quit()
                sys.exit()
                return

    def draw(self, surface):
        # Clear screen
        surface.fill((135, 206, 235))  # Sky blue background        
        self.start_button.draw(surface)
        self.quit_button.draw(surface)
        surface.blit(self.title, (SCREEN_WIDTH/2 - 920/2, 76))
        surface.blit(self.upper_left_branch, (0, 384)) # FIXME: Change to normal branch instead of image
        surface.blit(self.upper_left_branch, (0, 572)) # FIXME: Change to normal branch instead of image
        surface.blit(pygame.transform.flip(self.upper_left_branch, True, False), (SCREEN_WIDTH - 472, 384)) # FIXME: Change to normal branch instead of image
        surface.blit(pygame.transform.flip(self.upper_left_branch, True, False), (SCREEN_WIDTH - 472, 572)) # FIXME: Change to normal branch instead of image
        surface.blit(self.cucu, (SCREEN_WIDTH - 401, 288)) # FIXME: Change to normal branch instead of image
        surface.blit(self.cucu, (SCREEN_WIDTH - 401, 476)) # FIXME: Change to normal branch instead of image
        surface.blit(pygame.transform.flip(self.cucu, True, False), (328, 288)) # FIXME: Change to normal branch instead of image
        surface.blit(pygame.transform.flip(self.cucu, True, False), (328, 476)) # FIXME: Change to normal branch instead of image        
        