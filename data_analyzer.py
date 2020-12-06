import pygame
from bird import Bird
import numpy as np

class DataAnalyzer:
    def __init__(self, w, h, tracking_length, tracked):
        self.values = []
        self.max_length = tracking_length
        self.current_index = -1

        self.w = w
        self.h = h

        self.v = pygame.Vector2(0, 0)

        self.tracked_birds = tracked


    def track(self, w):
        self.current_index += 1
        if self.current_index == self.max_length:
            self.current_index = 0
        output = []

        for t in range(0, len(self.tracked_birds)):
            bird = w.birds[self.tracked_birds[t]]

            ps = []
            vs = []
            if len(w.targets) > 0:
                target = (w.targets[bird.current_target] - bird.old_p)
            else:
                target = pygame.Vector2(0,0)
            if target.length_squared() > 0:
                target = target.normalize()
            target *= Bird.target_weight
            for i in bird.neighbours:
                n = w.birds[i]
                found = False
                for j in range(0, len(n.neighbours)):
                    if bird.id == n.neighbours[j]:
                        ps.append(-n.p_measurements[j])
                        vs.append(n.v_measurements[j])
                        found = True
                if not found:
                    distance = n.p - bird.p + Bird.error_vector(n.p_std)
                    velocity = n.v + Bird.error_vector(n.v_std)
                    ps.append(distance)
                    vs.append(velocity)

            prediction = Bird.flock(ps, vs, ps, target, bird.old_v)

            value = (prediction-bird.v)

            average_length = 10
            if len(self.values) >= average_length:
                index = self.current_index
                for i in range(0, average_length-1):
                    index -= 1
                    if index < 0:
                        index = self.max_length-1
                    value += self.values[index][t]
                value = value/average_length
            output.append(value)
            if value.length() > 1:
                bird.marked = True
            else:
                bird.marked = False
        if len(self.values) < self.max_length:
            self.values.append(output)
        else:
            self.values[self.current_index] = output


    def draw(self, screen):
        screen.fill((0, 0, 0))

        distance = self.w/self.max_length

        # top = max(self.values)*1.01
        # bot = min(self.values)*0.99

        top = 5
        bot = 0
        color = (250, 250, 250)
        for tracked in range(0, len(self.tracked_birds)):
            points = []
            for i in range(self.current_index, -1, -1):
                x = self.w - ((self.current_index-i) * distance)
                y = ((top-self.values[i][tracked].length()) / (top-bot)) * self.h
                points.append((x, y))

            for i in range(len(self.values)-1, self.current_index, -1):
                x = self.w - ((self.current_index+(100-i)) * distance)
                y = ((top - self.values[i][tracked].length()) / (top - bot)) * self.h
                points.append((x, y))

            if tracked == len(self.tracked_birds)-1:
                color = (250, 0, 0)
            if len(points) > 1:
                pygame.draw.lines(screen, color, False, points)
