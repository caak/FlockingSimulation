import pygame
import random
import numpy


class Bird:

    # the main adjustable weights
    avoid_range = 100
    attraction_weight = 1
    avoidance_weight = 0.02
    alignment_weight = 5
    target_weight = 100

    neighborhood_size = 7

    # 2 distance units per time unit
    # This can be adjusted along with dt to test the impact of slow/fast acceleration
    max_speed = 2
    max_speed_squared = max_speed**2

    # Speed adjustment per step. This can be set to 1 to eliminate impact, but results in a problem with detecting non-flockers:
    # If 1, nonflockers will turn toward new target in 1 timestep, making them extremely easy to identify.
    # Adding some arbitrary turn rate, makes it harder to spot nonflockers.
    turn_rate_factor = 0.05

    # These last variables are used only for diagnostics
    equilibrium = 0.0

    attraction_sum = 0.0
    avoidance_sum = 0.0
    alignment_sum = 0.0
    target_sum = 0.0

    # construct a single bird
    def __init__(self, x, y, bird_id, p_std=1, v_std=1):
        self.p = pygame.Vector2(x, y)
        self.v = pygame.Vector2(0, 0)
        self.id = bird_id

        self.neighbours = []

        self.current_target = 0
        self.target_sequence = []

        self.p_measurements = []
        self.v_measurements = []
        self.p_std = p_std
        self.v_std = v_std

        self.old_p = self.p
        self.old_v = self.v

        self.marked = False

        self.time_since_target = 0


    def calculate_v(self, w):
        self.time_since_target += 1
        self_v_measurement = self.v

        v = Bird.flock(self.p_measurements, self.v_measurements, self.get_current_target(w), self_v_measurement)
        # v = Bird.flock(self.p_measurements, self.v_measurements, w.target*Bird.target_weight, self_v_measurement)
        return v

    # the main part of the flocking algorithm
    # it is written so it can be called "externally", with any inputs
    # this is necesary for CID, which needs to call it with a different set of measurements
    @staticmethod
    def flock(ps, vs, target, current_v):
        if len(ps) > 0:
            avoidance = Bird.calculate_avoidance(ps)

            alignment = Bird.calculate_alignment(vs)

            attraction = Bird.calculate_attraction(ps)

            Bird.equilibrium += (avoidance+attraction).length()

            Bird.attraction_sum += attraction.length()
            Bird.avoidance_sum += avoidance.length()
            Bird.alignment_sum += alignment.length()
            Bird.target_sum += target.length()

            new_v = (target + avoidance + alignment + attraction).normalize()*(Bird.turn_rate_factor) + current_v
        else:
            new_v = target.normalize()*(Bird.turn_rate_factor) + current_v

        if new_v.length_squared() > Bird.max_speed_squared:
            new_v = (new_v.normalize()*(Bird.max_speed))

        return new_v

    def update_p(self, dt):
        self.old_p = pygame.Vector2(self.p)
        self.p += self.v*dt

    # calculate the target rule
    # also responsible for updating current target
    def get_current_target(self, w):
        if len(self.target_sequence) > 0:
            target = self.target_sequence[self.current_target]-self.p
            if target.length_squared() < w.target_range**2:
                # reached target, need new target
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

    # select closest neighbors from the distance matrix of World
    def update_neighbours(self, world):
        sorted_birds = numpy.argsort(world.distances[self.id])
        if len(sorted_birds) > Bird.neighborhood_size:
            self.neighbours = sorted_birds[1:Bird.neighborhood_size+1]
        else:
            self.neighbours = sorted_birds[1:-1]

    # add generated noise to distance and velocity measuremnents
    def update_measurements(self, world):
        self.p_measurements = [pygame.Vector2(0,0)]*len(self.neighbours)
        self.v_measurements = [pygame.Vector2(0,0)]*len(self.neighbours)
        for i in range(0, len(self.neighbours)):
            n = world.birds[self.neighbours[i]]
            distance = (n.p - self.p)

            p_error = pygame.Vector2(world.p_errors[self.id][i*2], world.p_errors[self.id][(i*2)+1])
            v_error = pygame.Vector2(world.v_errors[self.id][i*2], world.v_errors[self.id][(i*2)+1])

            self.p_measurements[i] = distance + p_error
            self.v_measurements[i] = n.v + v_error

    # only used for diagnostics
    @staticmethod
    def reset_force_sums():
        Bird.attraction_sum = 0.0
        Bird.avoidance_sum = 0.0
        Bird.alignment_sum = 0.0
        Bird.target_sum = 0.0



