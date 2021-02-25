import pygame
import random
import numpy
from world import World
import time


class Bird:

    avoid_range = 100
    attraction_weight = 5
    avoidance_weight = 0.05
    alignment_weight = 100
    target_weight = 400

    neighborhood_size = 5
    max_speed = 2
    max_speed_squared = max_speed**2

    attraction_sum = 0.0
    avoidance_sum = 0.0
    alignment_sum = 0.0
    target_sum = 0.0

    turn_rate_factor = 2

    total_duration = 0.0

    def __init__(self, x, y, bird_id, p_std=1, v_std=1):
        self.p = pygame.Vector2(x, y)
        self.v = pygame.Vector2(0, 0)
        self.id = bird_id

        self.neighbours = []

        self.current_target = 0
        self.target_sequence = []

        self.p_measurements = [0]*Bird.neighborhood_size
        self.v_measurements = [0]*Bird.neighborhood_size
        self.p_std = p_std
        self.v_std = v_std

        self.old_p = self.p
        self.old_v = self.v

        self.marked = False

        self.time_since_target = 0


    def calculate_v(self, w):
        self.time_since_target += 1
        self_v_measurement = self.v #+ pygame.Vector2(w.v_errors[self.id][self.id], w.v_errors[self.id][self.id+1])
        v = Bird.flock(self.p_measurements, self.v_measurements, self.get_current_target(w), self_v_measurement)
        return v

    @staticmethod
    def flock(ps, vs, target, current_v):
        avoidance = Bird.calculate_avoidance(ps)

        alignment = Bird.calculate_alignment(vs)

        attraction = Bird.calculate_attraction(ps)

        Bird.attraction_sum += attraction.length()
        Bird.avoidance_sum += avoidance.length()
        Bird.alignment_sum += alignment.length()
        Bird.target_sum += target.length()

        # self.old_v = pygame.Vector2(self.v)

        new_v = (target + avoidance + alignment + attraction).normalize()*(Bird.turn_rate_factor) + current_v
        new_v = (new_v.normalize()*(Bird.max_speed))#*(Bird.turn_rate_factor * dt)
        # if new_v.length() > Bird.max_speed:
        #     new_v *= Bird.max_speed / new_v.length()

        return new_v#(new_v + current_v).normalize()*Bird.max_speed


    def update_p(self, dt):
        self.old_p = pygame.Vector2(self.p)
        self.p += self.v*dt

    def get_current_target(self, w):
        if len(self.target_sequence) > 0:
            target = self.target_sequence[self.current_target]-self.p
            if target.length_squared() < World.target_range**2:
                self.current_target += 1
                self.time_since_target = 0
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
                # This case helps break birds apart when stuck in the same position
                avoidance += pygame.Vector2((random.randint(0, 1) - 0.5) * 0.1, (random.randint(0, 1) - 0.5) * 0.1)
            elif length < Bird.avoid_range:

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
        for i in range(0, len(self.neighbours)):
            n = world.birds[self.neighbours[i]]
            distance = (n.p - self.p)
            start = time.thread_time_ns()
            p_error = pygame.Vector2(world.p_errors[self.id][i*2], world.p_errors[self.id][(i*2)+1])
            v_error = pygame.Vector2(world.v_errors[self.id][i*2], world.v_errors[self.id][(i*2)+1])
            Bird.total_duration += time.thread_time_ns()-start

            self.p_measurements[i] = distance + p_error
            self.v_measurements[i] = n.v + v_error
