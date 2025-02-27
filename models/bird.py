import pygame
from constants import BIRD_SIZE

class Bird:
    def __init__(self, color):
        self.color = color
        # Create a simple bird representation (circle for now)
        self.surface = pygame.Surface((BIRD_SIZE, BIRD_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, color, (BIRD_SIZE//2, BIRD_SIZE//2), BIRD_SIZE//2)
        
    def draw(self, surface, pos):
        surface.blit(self.surface, pos)
        
    def __eq__(self, other):
        if not isinstance(other, Bird):
            return False
        return self.color == other.color