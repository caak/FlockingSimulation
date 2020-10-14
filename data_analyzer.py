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
            attraction = pygame.Vector2(0, 0)
            alignment = pygame.Vector2(0, 0)
            avoidance = pygame.Vector2(0, 0)
            for i in range(0, len(bird.neighbours)):
                n = w.birds[bird.neighbours[i]]
                # distance = pygame.Vector2(0, 0)
                # v_distance = pygame.Vector2(0, 0)
                if bird.id in n.neighbours and n.id < len(w.birds)-1:
                    other_idx = np.where(n.neighbours == bird.id)[0][0]
                    distance = n.p_measurements[other_idx]
                    v_distance = n.old_v
                else:
                    distance = bird.old_p - n.old_p + Bird.error_vector(1)
                    v_distance = n.old_v

                attraction += -distance
                alignment += v_distance
                avoidance += distance.normalize() * (1 / distance.length())

            alignment = alignment/len(bird.neighbours) * Bird.alignment_weight
            attraction = attraction/len(bird.neighbours)* Bird.attraction_weight
            avoidance = avoidance * Bird.avoidance_weight

            prediction = pygame.Vector2(0, 0)
            prediction += avoidance
            prediction += alignment
            prediction += attraction

            if len(w.targets) > 0:
                target = (w.targets[bird.current_target] - bird.old_p)
                if target.length_squared() > 0:
                    target = target.normalize() * Bird.target_weight
                prediction += target

            prediction *= Bird.turn_rate_factor
            prediction += bird.old_v
            if prediction.length() > Bird.max_speed:
                prediction *= Bird.max_speed / prediction.length()

            value = (prediction-bird.v).length()
            if len(self.values) >= 10:
                recent = self.values[self.current_index-9:self.current_index]
                for r in recent:
                    value += r[t]
                value = value/10
            output.append(value)

        if len(self.values) < self.max_length:
            self.values.append(output)
        else:
            self.values[self.current_index] = output


    def draw(self, screen):
        screen.fill((0, 0, 0))

        distance = self.w/self.max_length

        # top = max(self.values)*1.01
        # bot = min(self.values)*0.99

        top = 200
        bot = 0
        colors = [(250, 250, 250), (250, 0, 0)]
        for tracked in range(0, len(self.tracked_birds)):
            points = []
            for i in range(self.current_index, -1, -1):
                x = self.w - ((self.current_index-i) * distance)
                y = ((top-self.values[i][tracked]) / (top-bot)) * self.h
                points.append((x, y))

            for i in range(len(self.values)-1, self.current_index, -1):
                x = self.w - ((self.current_index+(100-i)) * distance)
                y = ((top - self.values[i][tracked]) / (top - bot)) * self.h
                points.append((x, y))

            if len(points) > 1:
                pygame.draw.lines(screen, colors[tracked], False, points)