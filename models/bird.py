import pygame
import numpy as np
from global_vars import Globals
from animations.animation_manager import AnimationManager
from animations.animation import Animation

class Bird:
    def __init__(self, color, isMock=False):
        self.color = color
        # Create a simple bird representation (circle for now)
        self.surface = pygame.Surface((Globals.BIRD_SIZE, Globals.BIRD_SIZE), pygame.SRCALPHA)
        self.anims = AnimationManager()
        self.current_animation = None
        self.animation_finished = True
        
        if not isMock:
            bird_spritesheet = pygame.image.load("assets/cucu_fly_spritesheet.png")
            bird_spritesheet = bird_spritesheet.convert_alpha()  # Optimize for performance
            
            idle_jump_spritesheet = self.change_color(pygame.image.load("assets/idle_jump_spritesheet.png"), color)
            idle_jump_spritesheet = idle_jump_spritesheet.convert_alpha()  # Optimize for performance

            idle_spritesheet = self.change_color(pygame.image.load("assets/static_cucu.png"), color)
            idle_spritesheet = idle_spritesheet.convert_alpha()  # Optimize for performance
            
            self.sprite_sheet = self.change_color(bird_spritesheet, color)
            Globals.bird_height = bird_spritesheet.get_height()
            Globals.bird_width = bird_spritesheet.get_width() // 14 # FIXME: Should not be hardcoded
            self.anims.addAnimation(0, Animation(spritesheet=idle_spritesheet, frames_x=1, frames_y=1, frame_duration=5, row=1)) # Idle animation
            self.anims.addAnimation(1, Animation(spritesheet=idle_jump_spritesheet, frames_x=7, frames_y=1, frame_duration=0.1, row=1)) # Idle Jump animation
            self.anims.addAnimation(2, Animation(spritesheet=self.sprite_sheet, frames_x=14, frames_y=1, frame_duration=0.1, row=1)) # Fly animation

    def draw(self, surface, pos, flip=False):
        surface.blit(self.surface, pos)
        
        if self.animation_finished:
            self.current_animation = np.random.choice([0, 1], p=[0.9, 0.1])
            self.anims[self.current_animation].reset()
            self.animation_finished = False
        
        if self.anims[self.current_animation].is_finished():
            self.animation_finished = True
        
        self.anims.update(self.current_animation)
        self.anims.draw(surface, pos, flip)
        
    def __eq__(self, other):
        if not isinstance(other, Bird):
            return False
        return self.color == other.color
    
    def change_color(self, sprite, target_color):            
        # Convert the sprite surface to a numpy array (RGB)
        arr = pygame.surfarray.pixels3d(sprite)
        
        # Masks for specific colors
        mask_list = [
            np.all(arr == [121, 69, 56], axis=-1),   # Mask 0
            np.all(arr == [44, 13, 9], axis=-1),     # Mask 1
            np.all(arr == [89, 44, 32], axis=-1),    # Mask 2
            np.all(arr == [136, 88, 75], axis=-1),   # Mask 3
            np.all(arr == [191, 121, 94], axis=-1),  # Mask 4
            np.all(arr == [160, 98, 74], axis=-1),   # Mask 5
            np.all(arr == [188, 126, 101], axis=-1), # Mask 6
            np.all(arr == [186, 131, 109], axis=-1)  # Mask 7
        ]
                
        (r, g, b) = target_color
        darkness_factor = 1
        for i, mask in enumerate(mask_list):
            match (i):
                case 0:
                    darkness_factor = 0.6
                case 1:
                    darkness_factor = 0.2
                case 2:
                    darkness_factor = 0.5
                case 3 | 6:
                    darkness_factor = 0.8
                case 4:
                    darkness_factor = 1
                case 5:
                    darkness_factor = 0.7
                case 7:
                    darkness_factor = 1
            arr[mask] = [max(0, int(r * darkness_factor)), max(0, int(g * darkness_factor)), max(0, int(b * darkness_factor))]

        return sprite
