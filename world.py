import numpy as np
import pygame
import time

class World:
    target_range = 80

    def __init__(self, width, height):
        self.width, self.height = width, height
        self.birds = []
        self.targets = []
        self.distances = []
        self.p_errors = []
        self.v_errors = []

    def update(self, dt):
        self.calculate_distances()

        for bird in self.birds:
            bird.update_neighbours(self)
            bird.update_measurements(self)
            bird.old_v = bird.v

        for bird in self.birds:
            bird.v = bird.calculate_v(self)

        for bird in self.birds:
            bird.update_p(dt)

    def calculate_distances(self):
        if len(self.distances) < len(self.birds):
            self.distances = np.zeros((len(self.birds), len(self.birds)))

        for i in range(0, len(self.birds)):
            for j in range(0, len(self.birds)):
                distance = self.birds[i].p - self.birds[j].p
                self.distances[i][j] = distance.length_squared()

        self.p_errors = np.random.normal(0, 1, size=(len(self.birds), len(self.birds)*2))
        self.v_errors = np.random.normal(0, 1, size=(len(self.birds), len(self.birds)*2))
