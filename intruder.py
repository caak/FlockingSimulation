from bird import Bird
import pygame


class Follower(Bird):
    def __init__(self, x, y, bird_id, p_std=1, v_std=1):
        super().__init__(x, y, bird_id, p_std=p_std, v_std=v_std)


    def calculate_v(self, w):
        self.time_since_target += 1
        target = self.get_current_target(w)
        self_v_measurement = self.v
        return super().flock(self.p_measurements, self.v_measurements, pygame.Vector2(0,0), self_v_measurement)


class NonFlocker(Bird):
    def __init__(self, x, y, id, p_std=1, v_std=1):
        super().__init__(x, y, id, p_std, v_std)

    def calculate_v(self, w):
        self.time_since_target += 1
        new_v = (self.get_current_target(w).normalize())*(Bird.turn_rate_factor) + self.v

        # if new_v.length_squared() > 0.0:
        #     new_v = new_v.normalize() * Bird.max_speed
        return (new_v.normalize() * (Bird.max_speed))

class FormationBreaker(Bird):
    max_speed = Bird.max_speed*1.2
    y_dist = 0

    def __init__(self, x, y, id, p_std=1, v_std=1):
        super().__init__(x, y, id, p_std, v_std)
        self.target = pygame.Vector2(0.0, -1.0)
        self.a_id = id
        self.initiate_shift = False

    def calculate_v(self, w):
        self.time_since_target += 1
        new_v = (self.get_current_target(w).normalize())*(Bird.turn_rate_factor) + self.v

        # if new_v.length_squared() > 0.0:
        #     new_v = new_v.normalize() * Bird.max_speed
        return (new_v.normalize() * (Bird.max_speed if self.initiate_shift else FormationBreaker.max_speed))

    def get_current_target(self, w):
        return self.target*Bird.target_weight

    def update_p(self, dt):
        super().update_p(dt)
        if FormationBreaker.config.flock_center.y - 380 > self.p.y - (self.a_id*FormationBreaker.y_dist):
            shift = 0.1
            self.target = pygame.Vector2( -shift*2*(self.a_id%2) + shift, -1 )
            self.initiate_shift = True


def createAttackFormation(w, pos, c):
    count = 10
    height = 800
    FormationBreaker.y_dist = height/count

    for i in range(0, count):
        b = FormationBreaker(pos.x, pos.y+(i*FormationBreaker.y_dist), i)
        b.marked = True
        w.addBird(b)
    FormationBreaker.config = c