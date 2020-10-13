from world import World
from bird import Bird
from faulty_bird import FaultyBird
import pygame
import random

class TestSetup(World):
    def __init__(self, width, height):
        super().__init__(width, height)
        for i in range(0, 50):
            self.birds.append(Bird(200 + (i%2), 100 + (50 * i), i))
        for i in range(50, 53):
            self.birds.append(FaultyBird(200 + (i%2), 100 + (50 * i), i, 10, 1))

class HourGlass(World):
    def __init__(self, width, height, n):
        super().__init__(width, height)
        for i in range(0, n):
            self.birds.append(Bird(200 + (i%2), 100 + (50 * i), i))

        targets = [[200, 100], [600, 275], [1000, 100],
                   [1000, 600], [600, 425], [200, 600]]
        for t in targets:
            self.targets.append(pygame.Vector2(t[0], t[1]))
