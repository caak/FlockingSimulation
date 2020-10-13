from bird import Bird
import pygame


class FaultyBird(Bird):
    def __init__(self, x, y, id, p_error, v_error):
        super().__init__(x, y, id)
        self.v_std = v_error
        self.p_std = p_error


class NonFlocker(Bird):
    def __init__(self, x, y, id):
        super().__init__(x, y, id)

    def calculate_alignment(self, world):
        return pygame.Vector2(0, 0)

    def calculate_attraction(self, world):
        return pygame.Vector2(0, 0)

    def calculate_avoidance(self, world):
        return pygame.Vector2(0, 0)
