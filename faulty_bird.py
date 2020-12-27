from bird import Bird
import pygame


class FaultyBird(Bird):
    def __init__(self, x, y, id, p_error, v_error):
        super().__init__(x, y, id)
        self.v_std = v_error
        self.p_std = p_error

    def update_measurements(self, world):
        super().update_measurements(world)
        for i in range(0, len(self.p_measurements)):
            self.p_measurements[i] += pygame.Vector2(10, 10)

class NonFlocker(Bird):
    def __init__(self, x, y, id):
        super().__init__(x, y, id)

    def calculate_v(self, w):
        new_v = self.get_current_target(w)*Bird.turn_rate_factor
        new_v += self.v
        if new_v.length_squared() > 0.0:
            new_v = new_v.normalize() * Bird.max_speed
        return new_v

