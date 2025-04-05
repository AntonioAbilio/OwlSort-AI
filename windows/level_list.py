import pygame
from windows.state_manager import State
from levels.level_generator import LevelGenerator
from windows.birdsort import Game
from global_vars import Globals
from models.button import Button

# Level file paths
level_paths = [
    "levels/level_files/level1.cucu",  # Level 1
    "levels/level_files/level2.cucu",  # Level 2
    "levels/level_files/level3.cucu",  # Level 3
    "levels/level_files/level4.cucu",  # Level 4
    "levels/level_files/level5.cucu",  # Level 5
    "levels/level_files/level6.cucu",  # Level 6
    "levels/level_files/level7.cucu",  # Level 7
    "levels/level_files/level8.cucu",  # Level 8
    "levels/level_files/level9.cucu",  # Level 9
    "levels/level_files/level10.cucu", # Level 10
    "levels/level_files/level11.cucu", # Level 11
    "levels/level_files/level12.cucu"  # Level 12
]

class LevelList(State) :
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 70)
        self.text_surface = self.font.render("Choose Level", True, (0, 0, 0))
        
        # Background
        self.background = pygame.image.load("assets/forest_bg.png")
        self.background = pygame.transform.scale(self.background, (Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT))
        self.background = self.background.convert_alpha()  # Optimize for performance

        # Buttons
        offset = 100
        offset_up = 100
        col1 = Globals.SCREEN_WIDTH/2 - 250 - 180
        col2 = Globals.SCREEN_WIDTH/2 - 90
        col3 = Globals.SCREEN_WIDTH/2 + 250 
        button_width = 180
        button_height = 50
        button_color = Globals.BUTTON_COLOR
        hover_color = Globals.BUTTON_HOVER_COLOR
        self.go_back_button = Button(Globals.SCREEN_WIDTH/4 - 250, 100, 180, 50, "<= Go Back", button_color, hover_color)
        self.level1_button =  Button(col1, Globals.SCREEN_HEIGHT/2 - offset_up           , button_width, button_height, "Level 1" , button_color, hover_color)
        self.level2_button =  Button(col1, Globals.SCREEN_HEIGHT/2 - offset_up + offset  , button_width, button_height, "Level 2" , button_color, hover_color)
        self.level3_button =  Button(col1, Globals.SCREEN_HEIGHT/2 - offset_up + offset*2, button_width, button_height, "Level 3" , button_color, hover_color)
        self.level4_button =  Button(col1, Globals.SCREEN_HEIGHT/2 - offset_up + offset*3, button_width, button_height, "Level 4" , button_color, hover_color)
        self.level5_button =  Button(col2, Globals.SCREEN_HEIGHT/2 - offset_up           , button_width, button_height, "Level 5" , button_color, hover_color)
        self.level6_button =  Button(col2, Globals.SCREEN_HEIGHT/2 - offset_up + offset  , button_width, button_height, "Level 6" , button_color, hover_color)
        self.level7_button =  Button(col2, Globals.SCREEN_HEIGHT/2 - offset_up + offset*2, button_width, button_height, "Level 7" , button_color, hover_color)
        self.level8_button =  Button(col2, Globals.SCREEN_HEIGHT/2 - offset_up + offset*3, button_width, button_height, "Level 8" , button_color, hover_color)
        self.level9_button =  Button(col3, Globals.SCREEN_HEIGHT/2 - offset_up           , button_width, button_height, "Level 9" , button_color, hover_color)
        self.level10_button = Button(col3, Globals.SCREEN_HEIGHT/2 - offset_up + offset  , button_width, button_height, "Level 10", button_color, hover_color)
        self.level11_button = Button(col3, Globals.SCREEN_HEIGHT/2 - offset_up + offset*2, button_width, button_height, "Level 11", button_color, hover_color)
        self.level12_button = Button(col3, Globals.SCREEN_HEIGHT/2 - offset_up + offset*3, button_width, button_height, "Level 12", button_color, hover_color)

        self.level_button_list = [
            self.level1_button, self.level2_button, self.level3_button, self.level4_button,
            self.level5_button, self.level6_button, self.level7_button, self.level8_button,
            self.level9_button, self.level10_button, self.level11_button, self.level12_button
        ]
    
    def handle_event(self, event):
        levelGenerator = LevelGenerator()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Go back button
            if self.go_back_button.is_clicked(mouse_pos):
                from windows.choose_level import ChooseLevel
                self.next_state = ChooseLevel()
                return
            
            # Level buttons
            i = 0 # Level path index
            for button in self.level_button_list:
                if button.is_clicked(mouse_pos):
                    (level, color_counts, max_birds_per_branch) = levelGenerator.generate_level_from_file(level_paths[i])
                    self.next_state = Game(bird_list=level, num_branches=len(level), max_birds_per_branch=max_birds_per_branch, num_colors=color_counts)
                    return
                i += 1
            
    def draw(self, surface):
        # Draw background
        scaled_background = pygame.transform.scale(self.background, (surface.get_width(), surface.get_height()))
        surface.blit(scaled_background, (0, 0))  # Draw scaled background
        
        # Draw title
        surface.blit(self.text_surface, (Globals.SCREEN_WIDTH/2 - self.text_surface.get_width()/2, 150))
        
        # Draw go back button
        self.go_back_button.draw(surface)
        
        # Draw level buttons
        for button in self.level_button_list:
            button.draw(surface)
