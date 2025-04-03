import pygame
import sys
from levels import import_manager
from levels.level_generator import LevelGenerator
from windows.state_manager import State
from windows.birdsort import Game
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)
from models.button import Button

class ChooseLevel(State):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 70)
        self.background = pygame.image.load("assets/forest_bg.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.text_surface = self.font.render("Choose Level", True, (255, 255, 255))
        self.upper_left_branch = pygame.image.load("assets/branch.png")
        self.cucu = pygame.image.load("assets/static_cucu.png")
        self.go_back_button = Button(SCREEN_WIDTH/4 - 250, 100, 180, 50, "<= Go Back", (200, 200, 255), (150, 150, 255))
        self.levelList_button = Button(SCREEN_WIDTH/4 - 270, SCREEN_HEIGHT/2 - 50, 250, 50, "Level List", (200, 200, 255), (150, 150, 255))
        self.custom_button = Button(SCREEN_WIDTH/2 + SCREEN_WIDTH/4 + 20, SCREEN_HEIGHT/2 - 50, 250, 50, "Custom (Load from file)", (200, 200, 255), (150, 150, 255))
        self.loading = False  # To indicate if a level is being loaded

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
                if not self.loading:  # Prevent multiple clicks
                    self.loading = True
                    import_manager.load_level_threaded(self.on_level_loaded)
                return

    def on_level_loaded(self, result):
        """Callback function to handle the result of level loading."""
        self.loading = False  # Reset loading state
        if result is None:
            print("Failed to load level or invalid level data.")
            return

        (level, color_counts, max_birds_per_branch) = result
        game = Game(bird_list=level, max_birds_per_branch=max_birds_per_branch, num_branches=len(level), num_colors=color_counts) # FIXME: Make it not hard-coded
        if game.check_level_possible():
            print("Loaded Level:", level)  # Debugging print
            self.next_state = game
        else:
            print("Invalid level!")
        return
        
            
    def draw(self, surface):
        # Clear screen
        surface.blit(self.background, (0, 0))
        offset = 35  # TODO: Remove (TEMP)
  
        self.go_back_button.draw(surface)
        self.levelList_button.draw(surface)
        self.custom_button.draw(surface)
        surface.blit(self.text_surface, (SCREEN_WIDTH/2 - self.text_surface.get_width()/2, 150))
        surface.blit(self.upper_left_branch, (0, 384))  # FIXME: Change to normal branch instead of image
        surface.blit(pygame.transform.flip(self.upper_left_branch, True, False), (SCREEN_WIDTH - 472, 384))  # FIXME: Change to normal branch instead of image
        surface.blit(self.cucu, (SCREEN_WIDTH - 430, 288-offset))  # FIXME: Change to normal branch instead of image
        surface.blit(pygame.transform.flip(self.cucu, True, False), (280, 288-offset))  # FIXME: Change to normal branch instead of image
