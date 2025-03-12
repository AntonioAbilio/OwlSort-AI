import pygame
from levels import import_manager
from state_manager import State
from birdsort import Game
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
        self.levelList_button = Button(SCREEN_WIDTH/4 - 200, SCREEN_HEIGHT/2 - 50, 180, 50, "Level List", (200, 200, 255), (150, 150, 255))
        self.custom_button = Button(SCREEN_WIDTH/4 - 200, SCREEN_HEIGHT/2 - 50 + 188, 180, 50, "Custom (Load from file)", (200, 200, 255), (150, 150, 255))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if level list button was clicked
            if self.levelList_button.is_clicked(mouse_pos):
                self.next_state = Game(7)
                return

            # Check if custom button was clicked
            if self.custom_button.is_clicked(mouse_pos):
                level_data = import_manager.load_level()
                self.next_state = Game(num_branches=len(level_data), bird_list=level_data, is_custom=True)
                print("Loaded Level:", level_data)  # Debugging print
                #TODO: Deal with invalid levels (check if level_data is None)
                return

            
    def draw(self, surface):
        # Clear screen
        surface.fill((135, 206, 235))  # Sky blue background        
        self.levelList_button.draw(surface)
        self.custom_button.draw(surface)
        surface.blit(self.text_surface, (SCREEN_WIDTH/2 - self.text_surface.get_width()/2, 150))
        surface.blit(self.upper_left_branch, (0, 384)) # FIXME: Change to normal branch instead of image
        surface.blit(self.upper_left_branch, (0, 572)) # FIXME: Change to normal branch instead of image
        surface.blit(pygame.transform.flip(self.upper_left_branch, True, False), (SCREEN_WIDTH - 472, 384)) # FIXME: Change to normal branch instead of image
        surface.blit(pygame.transform.flip(self.upper_left_branch, True, False), (SCREEN_WIDTH - 472, 572)) # FIXME: Change to normal branch instead of image
        surface.blit(self.cucu, (SCREEN_WIDTH - 401, 288)) # FIXME: Change to normal branch instead of image
        surface.blit(self.cucu, (SCREEN_WIDTH - 401, 476)) # FIXME: Change to normal branch instead of image
        surface.blit(pygame.transform.flip(self.cucu, True, False), (328, 288)) # FIXME: Change to normal branch instead of image
        surface.blit(pygame.transform.flip(self.cucu, True, False), (328, 476)) # FIXME: Change to normal branch instead of image        
        