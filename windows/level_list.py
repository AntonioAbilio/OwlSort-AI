import pygame
from windows.state_manager import State
from levels.level_generator import LevelGenerator
from windows.birdsort import Game
from global_vars import Globals
from models.button import Button

# Level file paths
LEVEL1_CONFIG  =  "levels/level_files/level1.cucu"
LEVEL2_CONFIG  =  "levels/level_files/level2.cucu"
LEVEL3_CONFIG  =  "levels/level_files/level3.cucu"
LEVEL4_CONFIG  =  "levels/level_files/level4.cucu"
LEVEL5_CONFIG  =  "levels/level_files/level5.cucu"
LEVEL6_CONFIG  =  "levels/level_files/level6.cucu"
LEVEL7_CONFIG  =  "levels/level_files/level7.cucu"
LEVEL8_CONFIG  =  "levels/level_files/level8.cucu"
LEVEL9_CONFIG  =  "levels/level_files/level9.cucu"
LEVEL10_CONFIG =  "levels/level_files/level10.cucu"
LEVEL11_CONFIG =  "levels/level_files/level11.cucu"
LEVEL12_CONFIG =  "levels/level_files/level12.cucu"

class LevelList(State) :
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 70)
        self.text_surface = self.font.render("Choose Level", True, (0, 0, 0))
        self.background = pygame.image.load("assets/forest_bg.png")
        self.background = pygame.transform.scale(self.background, (Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT))
        offset = 100
        offset_up = 100
        col1 = Globals.SCREEN_WIDTH/2 - 250 - 180
        col2 = Globals.SCREEN_WIDTH/2 - 90
        col3 = Globals.SCREEN_WIDTH/2 + 250 
        self.go_back_button = Button(Globals.SCREEN_WIDTH/4 - 250, 100, 180, 50, "<= Go Back", (200, 200, 255), (150, 150, 255))
        self.level1_button =  Button(col1, Globals.SCREEN_HEIGHT/2 - offset_up           , 180, 50, "Level 1" , (200, 200, 255), (150, 150, 255))
        self.level2_button =  Button(col1, Globals.SCREEN_HEIGHT/2 - offset_up + offset  , 180, 50, "Level 2" , (200, 200, 255), (150, 150, 255))
        self.level3_button =  Button(col1, Globals.SCREEN_HEIGHT/2 - offset_up + offset*2, 180, 50, "Level 3" , (200, 200, 255), (150, 150, 255))
        self.level4_button =  Button(col1, Globals.SCREEN_HEIGHT/2 - offset_up + offset*3, 180, 50, "Level 4" , (200, 200, 255), (150, 150, 255))
        self.level5_button =  Button(col2, Globals.SCREEN_HEIGHT/2 - offset_up           , 180, 50, "Level 5" , (200, 200, 255), (150, 150, 255))
        self.level6_button =  Button(col2, Globals.SCREEN_HEIGHT/2 - offset_up + offset  , 180, 50, "Level 6" , (200, 200, 255), (150, 150, 255))
        self.level7_button =  Button(col2, Globals.SCREEN_HEIGHT/2 - offset_up + offset*2, 180, 50, "Level 7" , (200, 200, 255), (150, 150, 255))
        self.level8_button =  Button(col2, Globals.SCREEN_HEIGHT/2 - offset_up + offset*3, 180, 50, "Level 8" , (200, 200, 255), (150, 150, 255))
        self.level9_button =  Button(col3, Globals.SCREEN_HEIGHT/2 - offset_up           , 180, 50, "Level 9" , (200, 200, 255), (150, 150, 255))
        self.level10_button = Button(col3, Globals.SCREEN_HEIGHT/2 - offset_up + offset  , 180, 50, "Level 10", (200, 200, 255), (150, 150, 255))
        self.level11_button = Button(col3, Globals.SCREEN_HEIGHT/2 - offset_up + offset*2, 180, 50, "Level 11", (200, 200, 255), (150, 150, 255))
        self.level12_button = Button(col3, Globals.SCREEN_HEIGHT/2 - offset_up + offset*3, 180, 50, "Level 12", (200, 200, 255), (150, 150, 255))
    
    def handle_event(self, event):
        levelGenerator = LevelGenerator()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.go_back_button.is_clicked(mouse_pos):
                from windows.choose_level import ChooseLevel
                self.next_state = ChooseLevel()
                return
            
            if self.level1_button.is_clicked(mouse_pos):
                (level, color_counts, max_birds_per_branch) = levelGenerator.generate_level_from_file(LEVEL1_CONFIG)
                self.next_state = Game(bird_list=level, num_branches=len(level), max_birds_per_branch=max_birds_per_branch, num_colors=color_counts)
                return
            
            if self.level2_button.is_clicked(mouse_pos):
                (level, color_counts, max_birds_per_branch) = levelGenerator.generate_level_from_file(LEVEL2_CONFIG)
                self.next_state = Game(bird_list=level, num_branches=len(level), max_birds_per_branch=max_birds_per_branch, num_colors=color_counts)
                return
            
            if self.level3_button.is_clicked(mouse_pos):
                (level, color_counts, max_birds_per_branch) = levelGenerator.generate_level_from_file(LEVEL3_CONFIG)
                self.next_state = Game(bird_list=level, num_branches=len(level), max_birds_per_branch=max_birds_per_branch, num_colors=color_counts)
                return
            
            # TODO: This needs to be changed
            if self.level4_button.is_clicked(mouse_pos):
                (level, color_counts, max_birds_per_branch) = levelGenerator.generate_level_from_file(LEVEL3_CONFIG)
                self.next_state = Game(bird_list=level, num_branches=len(level), max_birds_per_branch=max_birds_per_branch, num_colors=color_counts)
                return
            
            # TODO: This needs to be changed
            if self.level5_button.is_clicked(mouse_pos):
                (level, color_counts, max_birds_per_branch) = levelGenerator.generate_level_from_file(LEVEL3_CONFIG)
                self.next_state = Game(bird_list=level, num_branches=len(level), max_birds_per_branch=max_birds_per_branch, num_colors=color_counts)
                return
            
            # TODO: This needs to be changed
            if self.level6_button.is_clicked(mouse_pos):
                (level, color_counts, max_birds_per_branch) = levelGenerator.generate_level_from_file(LEVEL3_CONFIG)
                self.next_state = Game(bird_list=level, num_branches=len(level), max_birds_per_branch=max_birds_per_branch, num_colors=color_counts)
                return
            
            # TODO: This needs to be changed
            if self.level7_button.is_clicked(mouse_pos):
                (level, color_counts, max_birds_per_branch) = levelGenerator.generate_level_from_file(LEVEL3_CONFIG)
                self.next_state = Game(bird_list=level, num_branches=len(level), max_birds_per_branch=max_birds_per_branch, num_colors=color_counts)
                return
            
            # TODO: This needs to be changed
            if self.level8_button.is_clicked(mouse_pos):
                (level, color_counts, max_birds_per_branch) = levelGenerator.generate_level_from_file(LEVEL3_CONFIG)
                self.next_state = Game(bird_list=level, num_branches=len(level), max_birds_per_branch=max_birds_per_branch, num_colors=color_counts)
                return
            
            # TODO: This needs to be changed
            if self.level9_button.is_clicked(mouse_pos):
                (level, color_counts, max_birds_per_branch) = levelGenerator.generate_level_from_file(LEVEL3_CONFIG)
                self.next_state = Game(bird_list=level, num_branches=len(level), max_birds_per_branch=max_birds_per_branch, num_colors=color_counts)
                return
            
            # TODO: This needs to be changed
            if self.level10_button.is_clicked(mouse_pos):
                (level, color_counts, max_birds_per_branch) = levelGenerator.generate_level_from_file(LEVEL3_CONFIG)
                self.next_state = Game(bird_list=level, num_branches=len(level), max_birds_per_branch=max_birds_per_branch, num_colors=color_counts)
                return
            
            # TODO: This needs to be changed
            if self.level11_button.is_clicked(mouse_pos):
                (level, color_counts, max_birds_per_branch) = levelGenerator.generate_level_from_file(LEVEL3_CONFIG)
                self.next_state = Game(bird_list=level, num_branches=len(level), max_birds_per_branch=max_birds_per_branch, num_colors=color_counts)
                return
            
            # TODO: This needs to be changed
            if self.level12_button.is_clicked(mouse_pos):
                (level, color_counts, max_birds_per_branch) = levelGenerator.generate_level_from_file(LEVEL3_CONFIG)
                self.next_state = Game(bird_list=level, num_branches=len(level), max_birds_per_branch=max_birds_per_branch, num_colors=color_counts)
                return
            
    def draw(self, surface):
        scaled_background = pygame.transform.scale(self.background, (surface.get_width(), surface.get_height()))
        surface.blit(scaled_background, (0, 0))  # Draw scaled background
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
        surface.blit(self.text_surface, (Globals.SCREEN_WIDTH/2 - self.text_surface.get_width()/2, 150))
        
  

