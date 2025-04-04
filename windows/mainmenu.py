import pygame
import sys
from windows.state_manager import State
from windows.choose_level import ChooseLevel
from global_vars import Globals
from models.button import Button

class MainMenu(State) :
    def __init__(self):
        super().__init__()
        self.title = pygame.image.load("assets/title.png")
        self.title = self.title.convert_alpha()  # Optimize for performance
        
        self.background = pygame.image.load("assets/forest_bg.png")
        self.background = pygame.transform.scale(self.background, (Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT))
        self.background = self.background.convert_alpha()  # Optimize for performance
        
        self.upper_left_branch = pygame.image.load("assets/branch.png")
        self.upper_left_branch = self.upper_left_branch.convert_alpha()  # Optimize for performance
        
        self.offset=-Globals.BIRD_SIZE+25
        self.cucu = pygame.image.load("assets/static_cucu.png")
        self.cucu = self.cucu.convert_alpha()  # Optimize for performance
        
        self.upper_margin = 2 * Globals.SCREEN_HEIGHT/5
        self.gap_between_branches_y = 188
        self.button_height = 50 
        self.button_width = 180
        self.start_button = Button(Globals.BRANCH_WIDTH/4, self.upper_margin - self.button_height, self.button_width, self.button_height, "Start", (200, 200, 255), (150, 150, 255))
        self.quit_button = Button(Globals.BRANCH_WIDTH/4, self.upper_margin - self.button_height + self.gap_between_branches_y, self.button_width, self.button_height, "Quit", (200, 200, 255), (150, 150, 255))
    
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

    def draw(self, surface):
        # Clear screen
        scaled_background = pygame.transform.scale(self.background, (surface.get_width(), surface.get_height()))
        surface.blit(scaled_background, (0, 0))  # Draw scaled background
        
        self.start_button.draw(surface)
        self.quit_button.draw(surface)
        surface.blit(self.title, (Globals.SCREEN_WIDTH/2 - 920/2, 76))
        surface.blit(self.upper_left_branch, (0, self.upper_margin))
        surface.blit(self.upper_left_branch, (0, self.upper_margin + self.gap_between_branches_y))
        surface.blit(pygame.transform.flip(self.upper_left_branch, True, False), (Globals.SCREEN_WIDTH - Globals.BRANCH_WIDTH, self.upper_margin))
        surface.blit(pygame.transform.flip(self.upper_left_branch, True, False), (Globals.SCREEN_WIDTH - Globals.BRANCH_WIDTH,  self.upper_margin + self.gap_between_branches_y))
        surface.blit(self.cucu, (Globals.SCREEN_WIDTH - Globals.BRANCH_WIDTH + Globals.BIRD_SIZE/2, self.upper_margin-self.offset))
        surface.blit(self.cucu, (Globals.SCREEN_WIDTH - Globals.BRANCH_WIDTH + Globals.BIRD_SIZE/2, self.upper_margin-self.offset-self.gap_between_branches_y))
        surface.blit(pygame.transform.flip(self.cucu, True, False), (Globals.BRANCH_WIDTH - 2*Globals.BIRD_SIZE - Globals.BIRD_SIZE/2, self.upper_margin-self.offset))
        surface.blit(pygame.transform.flip(self.cucu, True, False), (Globals.BRANCH_WIDTH - 2*Globals.BIRD_SIZE - Globals.BIRD_SIZE/2, self.upper_margin-self.offset-self.gap_between_branches_y))        
        