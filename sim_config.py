import pygame

class Config:
    def __init__(self):
        self.draw_groups = False
        self.pause = True
        self.iteration_count = 0
        self.camera = pygame.Vector2(0, 0)
        self.camera_offset = pygame.Vector2(0, 0)
        self.flock_center = pygame.Vector2(0.0, 0.0)
        self.avg_velocity = pygame.Vector2(0.0, 0.0)
        self.compass_pos = pygame.Vector2(50, 50)
        self.compass_radius = 50
        self.target = pygame.Vector2(0.0, 0.0)