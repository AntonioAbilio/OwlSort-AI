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
            
            idle_jump_spritesheet = self.tint_sprite(pygame.image.load("assets/idle_jump_spritesheet.png"), color)
            idle_jump_spritesheet = idle_jump_spritesheet.convert_alpha()  # Optimize for performance

            idle_spritesheet = self.tint_sprite(pygame.image.load("assets/static_cucu.png"), color)
            idle_spritesheet = idle_spritesheet.convert_alpha()  # Optimize for performance
            
            self.sprite_sheet = self.tint_sprite(bird_spritesheet, color)
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
    
    def tint_sprite(self, sprite, color):
        tinted_sprite = sprite.copy()  # Copy to avoid modifying the original

        # Create a solid color surface with the same size as the sprite
        tint_surface = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
        tint_surface.fill(color)  # Fill it with the tint color

        # Multiply the sprite by the tint color, keeping alpha intact
        tinted_sprite.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        return tinted_sprite
