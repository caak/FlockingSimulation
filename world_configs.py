from world import World
from bird import Bird
from faulty_bird import NonFlocker
import pygame
import random

class TestSetup(World):
    def __init__(self, width, height, n):
        super().__init__(width, height)
        for i in range(0, n):
            self.birds.append(Bird(200 + (i%2), 100 + (50 * i), i))


class HourGlass(World):
    def __init__(self, width, height, n):
        super().__init__(width, height)
        for i in range(0, n):
            self.birds.append(Bird(200 + ((i%2))*40, 300 + (15 * i), i))

        targets = [[200, 100], [600, 275], [1000, 100],
                   [1000, 600], [600, 425], [200, 600]]
        for t in targets:
            self.targets.append(pygame.Vector2(t[0], t[1]))

class Merge(World):
    def __init__(self, width, height, n, bad_count):
        super().__init__(width, height)
        for i in range(0, int(n/2)):
            self.birds.append(Bird(((i*-15)+((i%2))*40), 0 + (-15 * i)+((i%2))*12, i))

        for i in range(int(n/2), n):
            self.birds.append(Bird((((i-(n/2))*-15)+((i%2))*40), 600 + (15 * (i-(n/2)))+((i%2))*12, i))

        for i in range(0, int(bad_count/2)):
            self.birds.append(NonFlocker((((i * 5) * -17) - 71), -50 + (-40 * i) + ((i % 2)) * 12, n))
            n += 1

        for i in range(0, int(bad_count/2)):
            self.birds.append(NonFlocker((((i * 5) * -17) - 91), 650 + (40 * (i)) + ((i % 2)) * 12, n))
            n += 1

        targets = [[200, 350], [600, 350], [1000, 350], [2000, 350]]
        for t in targets:
            self.targets.append(pygame.Vector2(t[0], t[1]))