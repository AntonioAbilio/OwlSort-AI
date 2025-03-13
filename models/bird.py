import pygame
from constants import BIRD_SIZE
from animations.animation_manager import AnimationManager
from animations.animation import Animation

class Bird:
    def __init__(self, color):
        self.color = color
        # Create a simple bird representation (circle for now)
        self.surface = pygame.Surface((BIRD_SIZE, BIRD_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, color, (BIRD_SIZE//2, BIRD_SIZE//2), BIRD_SIZE//2)
        self.anims = AnimationManager()
        bird_spritesheet = pygame.image.load("assets/cucu_fly_spritesheet.png")
        self.anims.addAnimation(0, Animation(bird_spritesheet, frames_x=14, frames_y=1, frame_duration=0.1, row=1)) # Fly animation
        
    def draw(self, surface, pos):
        surface.blit(self.surface, pos)
        self.anims.draw(surface, pos)
        self.anims.update(0)
        
    def __eq__(self, other):
        if not isinstance(other, Bird):
            return False
        return self.color == other.color