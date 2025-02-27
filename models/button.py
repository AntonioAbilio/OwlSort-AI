import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.SysFont(None, 30)
        
    def draw(self, surface):
        # Check for mouse hover
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color
            
        # Draw button
        pygame.draw.rect(surface, self.current_color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        # Draw text
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)