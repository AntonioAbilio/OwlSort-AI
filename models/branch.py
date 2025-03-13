import pygame
import constants
from constants import (
    SCREEN_WIDTH,
    BRANCH_WIDTH,
    BRANCH_HEIGHT,
    BIRD_SIZE,
    MAX_BIRDS_PER_BRANCH,
)

class Branch:
    def __init__(self, x, y, id):
        if x < (SCREEN_WIDTH/2): self.side = "left"
        else: self.side = "right"
        self.x = x
        self.y = y
        self.birds = []
        self.rect = pygame.Rect(x, y, BRANCH_WIDTH, BRANCH_HEIGHT)
        self.is_completed = False
        self.id = id
    
    def add_bird(self, bird):
        if len(self.birds) < MAX_BIRDS_PER_BRANCH and not self.is_completed:
            self.birds.append(bird)
            return True
        return False
    
    def draw(self, surface):
        # Draw branch
        pygame.draw.rect(surface, (139, 69, 19), self.rect)  # Brown color for branch
        
        # Draw birds on branch
        if self.side == "left":
            for i, bird in enumerate(self.birds):
                bird_x = self.x - 60 + (i * (BIRD_SIZE + 10))
                bird_y = self.y - constants.bird_height
                bird.draw(surface, (bird_x, bird_y))
        
        else:
            for i, bird in enumerate(self.birds):
                bird_x = self.x + 120 - (40 + (i * (BIRD_SIZE + 10)))
                bird_y = self.y - constants.bird_height
                bird.draw(surface, (bird_x, bird_y))
        
    def check_completion(self):
        # Branch is complete if it has birds and all are the same color
        if not self.birds:
            return False
            
        first_color = self.birds[0].color
        if len(self.birds) == MAX_BIRDS_PER_BRANCH and all(bird.color == first_color for bird in self.birds):
            self.is_completed = True
            return True
        return False
    
    def __eq__(self, other):
        if not isinstance(other, Branch):
            return False
        if other.id != self.id:
            return False
        if len(self.birds) != len(other.birds):
            return False
        for i in range(len(self.birds)):
            if self.birds[i].color != other.birds[i].color:
                return False
        if self.side != other.side:
            return False
        return True