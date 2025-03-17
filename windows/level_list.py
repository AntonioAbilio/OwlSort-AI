import pygame
from levels import import_manager
from windows.state_manager import State
from windows.birdsort import Game
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)
from models.button import Button

LEVEL1_CONFIG =  6 #TODO: Change
LEVEL2_CONFIG =  7 #TODO: Change
LEVEL3_CONFIG =  7 #TODO: Change
LEVEL4_CONFIG =  7 #TODO: Change
LEVEL5_CONFIG =  7 #TODO: Change
LEVEL6_CONFIG =  7 #TODO: Change 
LEVEL7_CONFIG =  7 #TODO: Change 
LEVEL8_CONFIG =  7 #TODO: Change 
LEVEL9_CONFIG =  7 #TODO: Change 
LEVEL10_CONFIG = 7 #TODO: Change 
LEVEL11_CONFIG = 7 #TODO: Change 
LEVEL12_CONFIG = 7 #TODO: Change 

class LevelList(State) :
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 70)
        self.text_surface = self.font.render("Choose Level", True, (255, 255, 255))
        self.background = pygame.image.load("assets/forest_bg.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        offset = 100
        offset_up = 100
        col1 = SCREEN_WIDTH/2 - 250 - 180
        col2 = SCREEN_WIDTH/2 - 90
        col3 = SCREEN_WIDTH/2 + 250 
        self.go_back_button = Button(SCREEN_WIDTH/4 - 250, 100, 180, 50, "<= Go Back", (200, 200, 255), (150, 150, 255))
        self.level1_button =  Button(col1, SCREEN_HEIGHT/2 - offset_up           , 180, 50, "Level 1" , (200, 200, 255), (150, 150, 255))
        self.level2_button =  Button(col1, SCREEN_HEIGHT/2 - offset_up + offset  , 180, 50, "Level 2" , (200, 200, 255), (150, 150, 255))
        self.level3_button =  Button(col1, SCREEN_HEIGHT/2 - offset_up + offset*2, 180, 50, "Level 3" , (200, 200, 255), (150, 150, 255))
        self.level4_button =  Button(col1, SCREEN_HEIGHT/2 - offset_up + offset*3, 180, 50, "Level 4" , (200, 200, 255), (150, 150, 255))
        self.level5_button =  Button(col2, SCREEN_HEIGHT/2 - offset_up           , 180, 50, "Level 5" , (200, 200, 255), (150, 150, 255))
        self.level6_button =  Button(col2, SCREEN_HEIGHT/2 - offset_up + offset  , 180, 50, "Level 6" , (200, 200, 255), (150, 150, 255))
        self.level7_button =  Button(col2, SCREEN_HEIGHT/2 - offset_up + offset*2, 180, 50, "Level 7" , (200, 200, 255), (150, 150, 255))
        self.level8_button =  Button(col2, SCREEN_HEIGHT/2 - offset_up + offset*3, 180, 50, "Level 8" , (200, 200, 255), (150, 150, 255))
        self.level9_button =  Button(col3, SCREEN_HEIGHT/2 - offset_up           , 180, 50, "Level 9" , (200, 200, 255), (150, 150, 255))
        self.level10_button = Button(col3, SCREEN_HEIGHT/2 - offset_up + offset  , 180, 50, "Level 10", (200, 200, 255), (150, 150, 255))
        self.level11_button = Button(col3, SCREEN_HEIGHT/2 - offset_up + offset*2, 180, 50, "Level 11", (200, 200, 255), (150, 150, 255))
        self.level12_button = Button(col3, SCREEN_HEIGHT/2 - offset_up + offset*3, 180, 50, "Level 12", (200, 200, 255), (150, 150, 255))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.go_back_button.is_clicked(mouse_pos):
                from windows.choose_level import ChooseLevel
                self.next_state = ChooseLevel()
                return
            
            if self.level1_button.is_clicked(mouse_pos):
                self.next_state = Game(LEVEL1_CONFIG)
                return
            
            if self.level2_button.is_clicked(mouse_pos):
                self.next_state = Game(LEVEL2_CONFIG)
                return
            
            if self.level3_button.is_clicked(mouse_pos):
                self.next_state = Game(LEVEL3_CONFIG)
                return
            
            if self.level4_button.is_clicked(mouse_pos):
                self.next_state = Game(LEVEL4_CONFIG)
                return
            
            if self.level5_button.is_clicked(mouse_pos):
                self.next_state = Game(LEVEL5_CONFIG)
                return
            
            if self.level6_button.is_clicked(mouse_pos):
                self.next_state = Game(LEVEL6_CONFIG)
                return
            
            if self.level7_button.is_clicked(mouse_pos):
                self.next_state = Game(LEVEL7_CONFIG)
                return
            
            if self.level8_button.is_clicked(mouse_pos):
                self.next_state = Game(LEVEL8_CONFIG)
                return
            
            if self.level9_button.is_clicked(mouse_pos):
                self.next_state = Game(LEVEL9_CONFIG)
                return
            
            if self.level10_button.is_clicked(mouse_pos):
                self.next_state = Game(LEVEL10_CONFIG)
                return
            
            if self.level11_button.is_clicked(mouse_pos):
                self.next_state = Game(LEVEL11_CONFIG)
                return
            
            if self.level12_button.is_clicked(mouse_pos):
                self.next_state = Game(LEVEL12_CONFIG)
                return
            
    def draw(self, surface):
        # Clear screen
        #surface.fill((135, 206, 235))  # Sky blue background        
        surface.blit(self.background, (0, 0))
        self.go_back_button.draw(surface)
        self.level1_button.draw(surface)
        self.level2_button.draw(surface)
        self.level3_button.draw(surface)
        self.level4_button.draw(surface)
        self.level5_button.draw(surface)
        self.level6_button.draw(surface)
        self.level7_button.draw(surface)
        self.level8_button.draw(surface)
        self.level9_button.draw(surface)
        self.level10_button.draw(surface)
        self.level11_button.draw(surface)
        self.level12_button.draw(surface)
        surface.blit(self.text_surface, (SCREEN_WIDTH/2 - self.text_surface.get_width()/2, 150))
        