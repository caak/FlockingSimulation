import numpy as np
import bird
import pygame
import time

class World:
    target_range = 80

    def __init__(self, width, height):
        self.width, self.height = width, height
        self.birds = []
        self.targets = []
        self.distances = []
        self.positions = []
        self.equilibrium = 0.0
        self.p_errors = []
        self.v_errors = []
        self.v_sum = 0.0
        self.target = pygame.Vector2(0.1, -1)


    def update(self, dt):
        self.v_sum = pygame.Vector2(0.0, 0.0 )
        self.calculate_distances()

        for bird in self.birds:
            bird.update_neighbours(self)
            bird.update_measurements(self)
            bird.old_v = bird.v

        for bird in self.birds:
            bird.v = bird.calculate_v(self)
            self.v_sum += bird.v

        for bird in self.birds:
            bird.update_p(dt)
            self.positions[bird.id] = bird.p

    def calculate_distances(self):
        if len(self.distances) < len(self.birds):
            self.distances = np.zeros((len(self.birds), len(self.birds)))

        for i in range(0, len(self.birds)):
            for j in range(0, len(self.birds)):
                distance = self.birds[i].p - self.birds[j].p
                self.distances[i][j] = distance.length()

        if len(self.birds) > 1:

            self.p_errors = np.random.normal(0, 1, size=(len(self.birds), len(self.birds)*2))
            self.p_errors = np.multiply(self.p_errors, np.array(self.p_stds)[:, np.newaxis])
            self.v_errors = np.random.normal(0, 1, size=(len(self.birds), len(self.birds)*2))
            self.v_errors = np.multiply(self.v_errors, np.array(self.v_stds)[:, np.newaxis])

    def addBird(self, b):
        b.id = len(self.birds)
        if len(self.birds) == 0:
            self.birds = [b]
            self.p_stds = [0.0]
            self.v_stds = [0.0]
        else:
            self.birds += [b]
            self.p_stds = np.append(self.p_stds, 0.0)
            self.v_stds = np.append(self.v_stds, 0.0)

        if len(self.birds) <= bird.Bird.neighborhood_size:
            b.p_measurements = [0.0] * (len(self.birds)-1)
            b.v_measurements = [0.0] * (len(self.birds)-1)
        else:
            b.p_measurements = [0.0] * bird.Bird.neighborhood_size
            b.v_measurements = [0.0] * bird.Bird.neighborhood_size

        self.positions = [pygame.Vector2(0,0)]*len(self.birds)


