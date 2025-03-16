import pygame
import numpy as np
from constants import BIRD_SIZE
import constants
from animations.animation_manager import AnimationManager
from animations.animation import Animation

class Bird:
    def __init__(self, color, isMock=False):
        self.color = color
        # Create a simple bird representation (circle for now)
        self.surface = pygame.Surface((BIRD_SIZE, BIRD_SIZE), pygame.SRCALPHA)
        self.anims = AnimationManager()
        
        if not isMock:
            print("Loading bird spritesheet")
            bird_spritesheet = pygame.image.load("assets/cucu_fly_spritesheet.png")
            idle_jump_spritesheet = self.tint_sprite(pygame.image.load("assets/idle_jump_spritesheet.png"), color)
            self.sprite_sheet = self.tint_sprite(bird_spritesheet, color)
            constants.bird_height = bird_spritesheet.get_height()
            constants.bird_width = bird_spritesheet.get_width() // 14 # FIXME: Should not be hardcoded
            self.anims.addAnimation(0, Animation(spritesheet=self.sprite_sheet, frames_x=14, frames_y=1, frame_duration=0.1, row=1)) # Fly animation
            self.anims.addAnimation(1, Animation(spritesheet=idle_jump_spritesheet, frames_x=7, frames_y=1, frame_duration=0.1, row=1)) # Fly animation

    def draw(self, surface, pos, flip=False):
        surface.blit(self.surface, pos)
        self.anims.draw(surface, pos, flip)
        self.anims.update(1)
        
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
