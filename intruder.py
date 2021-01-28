from bird import Bird
import pygame


class Follower(Bird):
    def __init__(self, x, y, bird_id, p_std=1, v_std=1):
        super().__init__(x, y, bird_id, p_std=p_std, v_std=v_std)


    def calculate_v(self, w):
        self.time_since_target += 1
        target = self.get_current_target(w)

        return super().flock(self.p_measurements, self.v_measurements, pygame.Vector2(0,0), self.v)

    def update_measurements(self, world):
        super().update_measurements(world)
        # for i in range(0, len(self.p_measurements)):
        #     self.p_measurements[i] += pygame.Vector2(10, 10)

class NonFlocker(Bird):
    def __init__(self, x, y, id, p_std=1, v_std=1):
        super().__init__(x, y, id, p_std, v_std)

    def calculate_v(self, w):
        self.time_since_target += 1
        new_v = self.get_current_target(w)*Bird.turn_rate_factor
        new_v += self.v
        if new_v.length_squared() > 0.0:
            new_v = new_v.normalize() * Bird.max_speed
        return new_v

