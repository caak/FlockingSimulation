import pygame
import random
import numpy
from world import World


class Bird:

    attraction_weight = 8.0
    avoidance_weight = 2000.0
    alignment_weight = 0.1
    target_weight = 200

    neighborhood_size = 5
    max_speed = 250
    max_speed_squared = max_speed**2

    attraction_sum = 0.0
    avoidance_sum = 0.0
    alignment_sum = 0.0
    target_sum = 0.0

    turn_rate_factor = 0.1

    def __init__(self, x, y, bird_id):
        self.p = pygame.Vector2(x, y)
        self.v = pygame.Vector2(0, 0)
        self.id = bird_id

        self.neighbours = []

        self.current_target = 0

        self.p_measurements = []
        self.v_measurements = []
        self.p_std = 1
        self.v_std = 1

        self.old_p = self.p
        self.old_v = self.v

    def update_v(self, w):
        target = self.calculate_target(w)

        avoidance = self.calculate_avoidance(w)

        alignment = self.calculate_alignment(w)

        attraction = self.calculate_attraction(w)

        Bird.attraction_sum += attraction.length()
        Bird.avoidance_sum += avoidance.length()
        Bird.alignment_sum += alignment.length()
        Bird.target_sum += target.length()

        self.old_v = pygame.Vector2(self.v)

        self.v += (target + avoidance + alignment + attraction)*Bird.turn_rate_factor

        if self.v.length() > Bird.max_speed:
            self.v *= Bird.max_speed / self.v.length()


    def update_p(self, dt):
        self.old_p = pygame.Vector2(self.p)
        self.p += self.v*dt*0.002

    def calculate_target(self, w):
        if len(w.targets) > 0:
            target = w.targets[self.current_target]-self.p
            if target.length_squared() < World.target_range**2:
                self.current_target += 1
                if self.current_target == len(w.targets):
                    self.current_target = 0
            target = w.targets[self.current_target] - self.p
            if target.length_squared() > 0:
                target = target.normalize()
        else:
            target = pygame.Vector2(0, 0)

        return target * Bird.target_weight

    def calculate_avoidance(self, world):
        avoidance = pygame.math.Vector2(0, 0)
        for n in range(0, len(self.neighbours)):
            avoidance += self.calculate_neighbor_avoidance(n, world)

        return avoidance * Bird.avoidance_weight

    def calculate_neighbor_avoidance(self, n, world):
        distance = -self.p_measurements[n]
        if distance.length_squared() == 0:
            # This case helps break birds apart, stuck in the same position
            distance = pygame.Vector2((random.randint(0, 1) - 0.5) * 0.1, (random.randint(0, 1) - 0.5) * 0.1)
        else:
            distance = distance.normalize() * (1 / distance.length())
        return distance

    def calculate_alignment(self, world):
        alignment = pygame.math.Vector2(0, 0)
        for n in range(0, len(self.neighbours)):
            bird = world.birds[self.neighbours[n]]
            alignment += self.v_measurements[n]

        alignment = alignment/len(self.neighbours)

        return alignment * Bird.alignment_weight

    def calculate_attraction(self, world):
        attraction = pygame.math.Vector2(0, 0)

        for n in range(0, len(self.neighbours)):
            attraction += self.p_measurements[n]

        attraction /= len(self.p_measurements)

        return attraction * Bird.attraction_weight

    def update_neighbours(self, world):
        sorted_birds = numpy.argsort(world.distances[self.id])
        self.neighbours = sorted_birds[1:Bird.neighborhood_size+1]

    def update_measurements(self, world):
        ps = []
        vs = []
        for neighbor in self.neighbours:
            ps.append(world.birds[neighbor].p - self.p + Bird.error_vector(self.p_std))
            vs.append(world.birds[neighbor].v + Bird.error_vector(self.v_std))

        self.p_measurements = ps
        self.v_measurements = vs

    @staticmethod
    def error_vector(std):
        return pygame.Vector2(numpy.random.normal(0, std), numpy.random.normal(0, std))
