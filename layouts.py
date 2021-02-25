from world import World
from bird import Bird
from intruder import NonFlocker, Follower
import pygame
import random
import math
import numpy as np

class TestSetup(World):
    def __init__(self, width, height, n):
        super().__init__(width, height)
        for i in range(0, n):
            self.birds.append(Bird(200 + (i%2), 100 + (50 * i), i))


class HourGlass(World):
    def __init__(self, width, height, good_count, bad_count, p_std=1, v_std=1, intruder_type=NonFlocker):
        super().__init__(width, height)
        targets = [[200, 100], [600, 275], [1000, 100],
                   [1000, 600], [600, 425], [200, 600]]
        for t in targets:
            self.targets.append(pygame.Vector2(t[0], t[1]))

        y_max_distance = 1000
        good_y_distance = y_max_distance/good_count
        bad_y_distance = (y_max_distance-300)/bad_count

        for i in range(0, good_count):
            bird = Bird(200 + ((i%2))*40, 300 + (good_y_distance * i), i, p_std=p_std, v_std=v_std)
            bird.target_sequence = self.targets
            self.birds.append(bird)

        for i in range(0, bad_count):
            bird = intruder_type(200 + (i % 2) * 40, 700 + (bad_y_distance * i), i + good_count, p_std=p_std, v_std=v_std)
            bird.target_sequence = self.targets
            self.birds.append(bird)

        self.p_stds = np.full(good_count + bad_count, p_std)
        self.v_stds = np.full(good_count + bad_count, v_std)



class Merge(World):
    def __init__(self, width, height, good_count, bad_count, p_std=1, v_std=1, intruder_type=NonFlocker):
        super().__init__(width, height)
        targets = [[200, 350], [600, 350], [1000, 350], [10000, 350]]
        for t in targets:
            self.targets.append(pygame.Vector2(t[0], t[1]))

        for i in range(0, int(good_count/2)):
            bird = Bird(((i * -15) + (i % 2) * 40), 0 + (-15 * i) + (i % 2) * 12, i, p_std, v_std)
            bird.target_sequence = self.targets
            self.birds.append(bird)

        for i in range(int(good_count/2), good_count):
            bird = Bird((((i-(good_count/2))*-15)+((i%2))*40), 600 + (15 * (i-(good_count/2)))+((i%2))*12, i, p_std, v_std)
            bird.target_sequence = self.targets
            self.birds.append(bird)

        n = good_count

        for i in range(0, int(bad_count/2)):
            bird = intruder_type((((i * 5) * -17) - 71), -50 + (-40 * i) + ((i % 2)) * 12, n, p_std, v_std)
            bird.target_sequence = self.targets
            self.birds.append(bird)
            n += 1

        for i in range(0, int(bad_count/2)):
            bird = intruder_type((((i * 5) * -17) - 91), 650 + (40 * (i)) + ((i % 2)) * 12, n, p_std, v_std)
            bird.target_sequence = self.targets

            self.birds.append(bird)
            n += 1

        self.p_stds = np.full(good_count + bad_count, p_std)
        self.v_stds = np.full(good_count + bad_count, v_std)


class Circle(World):
    def __init__(self, width, height, good_count, bad_count, p_std=1, v_std=1, intruder_type=NonFlocker, radius=400, target_count=5):
        super().__init__(width, height)
        for i in range(0, good_count):
            self.birds.append(Bird(200 + ((i%2))*40, 500 + (15 * i), i, p_std=1, v_std=1))

        for i in range(0, bad_count):
            self.birds.append(intruder_type(200 + ((i % 2)) * 40, 550 + (65 * i), i + good_count, p_std=1, v_std=1))

        if target_count == 1:
            self.targets.append(pygame.Vector2(width/2, height/2))
        else:
            initial_x = width/2
            initial_y = (height/2)
            step_length = (2*math.pi)/target_count
            for i in range(0, target_count):
                x = initial_x - (math.cos(i*step_length) * radius)
                y = initial_y - (math.sin(i*step_length) * radius)
                self.targets.append(pygame.Vector2(x, y))

        for bird in self.birds:
            bird.target_sequence = self.targets

        self.p_stds = np.full(good_count + bad_count, p_std)
        self.v_stds = np.full(good_count + bad_count, v_std)

class DualCircle(World):
    def __init__(self, width, height, good_count, bad_count):
        super().__init__(width, height)

        targets = [[200, 100], [600, 250], [200, 600],
                   [600, 450], [1000, 100], [1000, 600]]
        for t in targets:
            self.targets.append(pygame.Vector2(t[0], t[1]))
        left_targets = [self.targets[3], self.targets[1], self.targets[0], self.targets[2]]
        right_targets =[self.targets[3], self.targets[1], self.targets[4], self.targets[5]]

        for i in range(0, good_count):
            bird = Bird(600 + (50 * (i%2)), 600 + (25 * i), i)
            if i%2 == 0:
                bird.target_sequence.extend(left_targets)
            else:
                bird.target_sequence.extend(right_targets)
            self.birds.append(bird)


        for i in range(0, bad_count):
            bird = NonFlocker(200 + ((i % 2)) * 40, 350 + (65 * i), i+good_count)
            if i%2 == 0:
                bird.target_sequence.extend(left_targets)
            else:
                bird.target_sequence.extend(right_targets)
            self.birds.append(bird)


