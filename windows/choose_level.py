import pygame
import sys
from levels import import_manager
from levels.level_generator import LevelGenerator
from windows.state_manager import State
from windows.birdsort import Game
from global_vars import Globals
from models.button import Button

class ChooseLevel(State):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 70)
        self.background = pygame.image.load("assets/forest_bg.png")
        self.background = pygame.transform.scale(self.background, (Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT))
        self.background = self.background.convert_alpha()  # Optimize for performance

        self.text_surface = self.font.render("Choose Level", True, (0, 0, 0))
        self.text_surface = self.text_surface.convert_alpha()  # Optimize for performance

        self.branch_margin = 0
        self.gap_between_branches_y = 188
        self.upper_margin = 2 * Globals.SCREEN_HEIGHT/5
        self.upper_left_branch = pygame.image.load("assets/branch.png")
        self.upper_left_branch = self.upper_left_branch.convert_alpha()  # Optimize for performance
        
        self.offset=-Globals.BIRD_SIZE+25
        self.cucu = pygame.image.load("assets/static_cucu.png")
        self.cucu = self.cucu.convert_alpha()  # Optimize for performance

        self.button_width = 180
        self.button_width2 = 250
        self.button_height = 50
        self.go_back_button = Button(Globals.SCREEN_WIDTH/4 - 250, 100, 180, 50, "<= Go Back", Globals.BUTTON_COLOR, Globals.BUTTON_HOVER_COLOR)
        self.levelList_button = Button(Globals.MOCK_BRANCH_WIDTH/4, self.upper_margin - self.button_height, self.button_width, self.button_height, "Level List", Globals.BUTTON_COLOR,Globals.BUTTON_HOVER_COLOR)
        self.custom_button = Button(Globals.SCREEN_WIDTH - Globals.MOCK_BRANCH_WIDTH + 2*self.button_width2/3, self.upper_margin - self.button_height, self.button_width2, self.button_height, "Custom (Load from file)", Globals.BUTTON_COLOR, Globals.BUTTON_HOVER_COLOR)
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
        # Draw background
        scaled_background = pygame.transform.scale(self.background, (surface.get_width(), surface.get_height()))
        surface.blit(scaled_background, (0, 0))  # Draw scaled background
        
        # Draw title
        surface.blit(self.text_surface, (Globals.SCREEN_WIDTH/2 - self.text_surface.get_width()/2, 150))
  
        # Draw buttons
        self.go_back_button.draw(surface)
        self.levelList_button.draw(surface)
        self.custom_button.draw(surface)
        
        # Draw branches
        surface.blit(self.upper_left_branch, (0, self.upper_margin))
        surface.blit(pygame.transform.flip(self.upper_left_branch, True, False), (Globals.SCREEN_WIDTH - Globals.MOCK_BRANCH_WIDTH + self.branch_margin, self.upper_margin))
        
        # Draw birds
        surface.blit(self.cucu, (Globals.SCREEN_WIDTH - Globals.MOCK_BRANCH_WIDTH + Globals.BIRD_SIZE/2, self.upper_margin-self.offset-self.gap_between_branches_y))
        surface.blit(pygame.transform.flip(self.cucu, True, False), (Globals.MOCK_BRANCH_WIDTH - 2*Globals.BIRD_SIZE - Globals.BIRD_SIZE/2, self.upper_margin-self.offset-self.gap_between_branches_y))
