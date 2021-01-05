import pygame
import random
import numpy
from world import World


class Bird:

    avoid_range = 100
    attraction_weight = 10.0
    avoidance_weight = 0.05
    alignment_weight = 2
    target_weight = 200

    neighborhood_size = 5
    max_speed = 200
    max_speed_squared = max_speed**2

    attraction_sum = 0.0
    avoidance_sum = 0.0
    alignment_sum = 0.0
    target_sum = 0.0

    turn_rate_factor = 0.05

    def __init__(self, x, y, bird_id):
        self.p = pygame.Vector2(x, y)
        self.v = pygame.Vector2(0, 0)
        self.id = bird_id

        self.neighbours = []

        self.current_target = 0
        self.target_sequence = []

        self.p_measurements = []
        self.v_measurements = []
        self.p_std = 1
        self.v_std = 1

        self.old_p = self.p
        self.old_v = self.v

        self.marked = False


    def calculate_v(self, w):
        v = Bird.flock(self.p_measurements, self.v_measurements, self.get_current_target(w), self.v)
        return v

    @staticmethod
    def flock(ps, vs, target, current_v):

        # target = self.calculate_target(w)

        avoidance = Bird.calculate_avoidance(ps)

        alignment = Bird.calculate_alignment(vs)

        attraction = Bird.calculate_attraction(ps)

        Bird.attraction_sum += attraction.length()
        Bird.avoidance_sum += avoidance.length()
        Bird.alignment_sum += alignment.length()
        Bird.target_sum += target.length()

        # self.old_v = pygame.Vector2(self.v)

        new_v = (target + avoidance + alignment + attraction)*Bird.turn_rate_factor
        new_v += current_v
        # if new_v.length() > Bird.max_speed:
        #     new_v *= Bird.max_speed / new_v.length()

        return new_v.normalize()*Bird.max_speed


    def update_p(self, dt):
        self.old_p = pygame.Vector2(self.p)
        self.p += self.v*dt*0.002

    def get_current_target(self, w):
        if len(self.target_sequence) > 0:
            target = self.target_sequence[self.current_target]-self.p
            if target.length_squared() < World.target_range**2:
                self.current_target += 1
                if self.current_target == len(self.target_sequence):
                    self.current_target = 0
            target = self.target_sequence[self.current_target] - self.p
            if target.length_squared() > 0:
                target = target.normalize()
        else:
            target = pygame.Vector2(0, 0)

        return target * Bird.target_weight

    @staticmethod
    def calculate_avoidance(ps):
        avoidance = pygame.math.Vector2(0, 0)
        for distance in ps:
            length = distance.length()
            if length == 0:
                # This case helps break birds apart, stuck in the same position
                avoidance += pygame.Vector2((random.randint(0, 1) - 0.5) * 0.1, (random.randint(0, 1) - 0.5) * 0.1)
            elif length < Bird.avoid_range:
            # else:
                # avoidance += (-distance).normalize() / distance.length()
                avoidance += -distance * (Bird.avoid_range-length)

        return avoidance * Bird.avoidance_weight

    @staticmethod
    def calculate_alignment(vs):
        alignment = pygame.math.Vector2(0, 0)
        for v in vs:
            alignment += v

        alignment = alignment/len(vs)

        return alignment * Bird.alignment_weight

    @staticmethod
    def calculate_attraction(ps):
        attraction = pygame.math.Vector2(0, 0)

        for distance in ps:
            attraction += distance

        attraction /= len(ps)

        return attraction * Bird.attraction_weight

    def update_neighbours(self, world):
        sorted_birds = numpy.argsort(world.distances[self.id])
        self.neighbours = sorted_birds[1:Bird.neighborhood_size+1]

    def update_measurements(self, world):
        ps = []
        vs = []
        for neighbor in self.neighbours:
            n = world.birds[neighbor]
            distance = (n.p - self.p)
            error_factor = distance.length() * 0.05
            p_error = error_factor * Bird.error_vector(self.p_std)
            v_error = error_factor * Bird.error_vector(self.v_std)

            ps.append(distance + p_error)
            vs.append(n.v + v_error)

        self.p_measurements = ps
        self.v_measurements = vs

    @staticmethod
    def error_vector(std):
        return pygame.Vector2(numpy.random.normal(0, std), numpy.random.normal(0, std))
