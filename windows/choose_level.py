import pygame
import sys
from levels import import_manager
from windows.state_manager import State
from windows.birdsort import Game
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)
from models.button import Button

class ChooseLevel(State) :
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 70)
        self.text_surface = self.font.render("Choose Level", True, (255, 255, 255))
        self.upper_left_branch = pygame.image.load("assets/branch.png")
        self.cucu = pygame.image.load("assets/static_cucu.png")
        self.go_back_button = Button(SCREEN_WIDTH/4 - 250, 100, 180, 50, "<= Go Back", (200, 200, 255), (150, 150, 255))
        self.levelList_button = Button(SCREEN_WIDTH/4 - 270, SCREEN_HEIGHT/2 - 50, 250, 50, "Level List", (200, 200, 255), (150, 150, 255))
        self.custom_button = Button(SCREEN_WIDTH/2 + SCREEN_WIDTH/4 + 20, SCREEN_HEIGHT/2 - 50, 250, 50, "Custom (Load from file)", (200, 200, 255), (150, 150, 255))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.go_back_button.is_clicked(mouse_pos):
                from windows.mainmenu import MainMenu
                self.next_state = MainMenu()
                return
            
            # Check if level list button was clicked
            if self.levelList_button.is_clicked(mouse_pos):
                from windows.level_list import LevelList 
                self.next_state = LevelList()
                return

            # Check if custom button was clicked
            if self.custom_button.is_clicked(mouse_pos):
                result = import_manager.load_level()
                if result is None:
                    return
                (num_colors, level_data) = result
                game = Game(num_branches=len(level_data), bird_list=level_data, is_custom=True, num_colors=num_colors)
                if game.check_level_possible():
                    print("Loaded Level:", level_data)  # Debugging print
                    self.next_state = game
                else:
                    print("Invalid level!")
                return

            
    def draw(self, surface):
        # Clear screen
        surface.fill((135, 206, 235))  # Sky blue background        
        self.go_back_button.draw(surface)
        self.levelList_button.draw(surface)
        self.custom_button.draw(surface)
        surface.blit(self.text_surface, (SCREEN_WIDTH/2 - self.text_surface.get_width()/2, 150))
        surface.blit(self.upper_left_branch, (0, 384)) # FIXME: Change to normal branch instead of image
        surface.blit(pygame.transform.flip(self.upper_left_branch, True, False), (SCREEN_WIDTH - 472, 384)) # FIXME: Change to normal branch instead of image
        surface.blit(self.cucu, (SCREEN_WIDTH - 401, 288)) # FIXME: Change to normal branch instead of image
        surface.blit(pygame.transform.flip(self.cucu, True, False), (328, 288)) # FIXME: Change to normal branch instead of image
        