from world import World
from bird import Bird
from intruder import NonFlocker, Follower
import pygame
import random
import math

class TestSetup(World):
    def __init__(self, width, height, n):
        super().__init__(width, height)
        for i in range(0, n):
            self.birds.append(Bird(200 + (i%2), 100 + (50 * i), i))


class HourGlass(World):
    def __init__(self, width, height, good_count, bad_count, p_std=1, v_std=1, faulty_type=NonFlocker):
        super().__init__(width, height)
        targets = [[200, 100], [600, 275], [1000, 100],
                   [1000, 600], [600, 425], [200, 600]]
        for t in targets:
            self.targets.append(pygame.Vector2(t[0], t[1]))

        for i in range(0, good_count):
            bird = Bird(200 + ((i%2))*40, 300 + (15 * i), i, p_std=p_std, v_std=v_std)
            bird.target_sequence = self.targets
            self.birds.append(bird)

        for i in range(0, bad_count):
            bird = faulty_type(200 + ((i % 2)) * 40, 350 + (65 * i), i+good_count, p_std=p_std, v_std=v_std)
            bird.target_sequence = self.targets
            self.birds.append(bird)




class Merge(World):
    def __init__(self, width, height, n, bad_count):
        super().__init__(width, height)
        targets = [[200, 350], [600, 350], [1000, 350], [10000, 350]]
        for t in targets:
            self.targets.append(pygame.Vector2(t[0], t[1]))

        for i in range(0, int(n/2)):
            bird = Bird(((i * -15) + (i % 2) * 40), 0 + (-15 * i) + (i % 2) * 12, i)
            bird.target_sequence = self.targets
            self.birds.append(bird)

        for i in range(int(n/2), n):
            bird = Bird((((i-(n/2))*-15)+((i%2))*40), 600 + (15 * (i-(n/2)))+((i%2))*12, i)
            bird.target_sequence = self.targets
            self.birds.append(bird)

        for i in range(0, int(bad_count/2)):
            bird = NonFlocker((((i * 5) * -17) - 71), -50 + (-40 * i) + ((i % 2)) * 12, n)
            bird.target_sequence = self.targets
            self.birds.append(bird)
            n += 1

        for i in range(0, int(bad_count/2)):
            bird = NonFlocker((((i * 5) * -17) - 91), 650 + (40 * (i)) + ((i % 2)) * 12, n)
            bird.target_sequence = self.targets

            self.birds.append(bird)
            n += 1


class Circle(World):
    def __init__(self, width, height, good_count, bad_count, target_count, radius=400):
        super().__init__(width, height)
        for i in range(0, good_count):
            self.birds.append(Bird(200 + ((i%2))*40, 500 + (15 * i), i))

        for i in range(0, bad_count):
            self.birds.append(NonFlocker(200 + ((i % 2)) * 40, 550 + (65 * i), i+good_count))

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


