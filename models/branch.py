import pygame
from global_vars import Globals

class Branch:
    def __init__(self, x, y, id, isMock=False):
        if x < (Globals.SCREEN_WIDTH/2): self.side = "left"
        else: self.side = "right"
        self.x = x 
        self.y = y
        self.birds = []
        self.rect = pygame.Rect(x, y-100, Globals.BRANCH_WIDTH, Globals.BRANCH_HEIGHT+100)
        
        if not isMock:
            self.branch_sprite = pygame.image.load("assets/long_branch.png")   
        
        self.is_completed = False
        self.id = id
    
    def add_bird(self, bird):
        #if len(self.birds) < MAX_BIRDS_PER_BRANCH and not self.is_completed: #TODO: Remove
        self.birds.append(bird)
        return True
        #return False #TODO: Remove
    
    def draw(self, surface):
        # Draw branch
        if (self.side == "left"):
            surface.blit(self.branch_sprite, (self.x, self.y))
        else:
            surface.blit(pygame.transform.flip(self.branch_sprite, True, False), (self.x, self.y))

        # Draw birds on branch
        if self.side == "left":
            for i, bird in enumerate(self.birds):
                bird_x = (i * (Globals.BIRD_SIZE + 10))
                bird_y = self.y - Globals.bird_height - 5
                bird.draw(surface, (bird_x, bird_y), flip=True)
    
        else:
            for i, bird in enumerate(self.birds):
                bird_x = Globals.SCREEN_WIDTH - 120 - (40 + (i * (Globals.BIRD_SIZE + 10)))
                bird_y = self.y - Globals.bird_height - 5
                bird.draw(surface, (bird_x, bird_y))
        
    def check_completion(self):
        # Branch is complete if it has birds and all are the same color
        if not self.birds:
            return False
            
        first_color = self.birds[0].color
        if len(self.birds) == Globals.MAX_BIRDS_PER_BRANCH and all(bird.color == first_color for bird in self.birds):
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