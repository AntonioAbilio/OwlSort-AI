import pygame
import constants

class Animation:
    def __init__(self, spritesheet, frames_x, frames_y, frame_duration, row=1):
        self.spritesheet = spritesheet 
        self.frame_duration = frame_duration
        self.frame_time_left = frame_duration
        self.num_frames = frames_x
        self.frame = 0
        self.active = True
        self.source_rects = []
        frame_width = self.spritesheet.get_width() // frames_x
        frame_height = self.spritesheet.get_height() // frames_y
        
        for i in range(0,frames_x):
            x = i*frame_width
            y = (row-1)*frame_height
            self.source_rects.append(pygame.Rect(x, y, frame_width, frame_height))

    def stop(self):
        self.active = False
        
    def start(self):
        self.active = True
    
    def reset(self):
        self.frame = 0
        self.frame_time_left = self.frame_duration 

    def update(self):
        if (not self.active):
            return
        self.frame_time_left -= constants.delta_time
        if (self.frame_time_left <= 0):
            self.frame_time_left += self.frame_duration
            self.frame = (self.frame + 1)%self.num_frames

    def get_current_frame(self):
        return self.frames[self.current_frame]
    
    def draw(self, surface, pos):
        if (not self.active):
            return
        surface.blit(self.spritesheet, pos, self.source_rects[self.frame])
    
    