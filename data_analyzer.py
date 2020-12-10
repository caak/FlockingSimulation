import pygame
from bird import Bird
import numpy as np
import faulty_bird

class DataAnalyzer:
    def __init__(self, w, h, tracking_length, good_count, bad_count):
        self.values = []
        self.max_length = tracking_length
        self.current_index = -1

        self.w = w
        self.h = h

        self.v = pygame.Vector2(0, 0)

        self.good_count = good_count
        self.bad_count = bad_count

        self.avg_error = 0.0
        self.median_error = 0.0

        self.treshold_multiplier = 3

        self.FP = 0
        self.TP = 0
        self.FN = 0
        self.TN = 0

    def reset_confusion_matrix(self):
        self.FP = 0
        self.TP = 0
        self.FN = 0
        self.TN = 0

    def track(self, w):
        self.current_index += 1
        if self.current_index == self.max_length:
            self.current_index = 0
        output = []

        for t in range(0, self.good_count + self.bad_count):
            bird = w.birds[t]

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

            value = (prediction-bird.v).length()

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
        if len(self.values) < self.max_length:
            self.values.append(output)
        else:
            self.values[self.current_index] = output

        self.avg_error = 0
        for value in output:
            self.avg_error += value
        self.avg_error /= len(w.birds)

        self.median_error = sorted(output)[int(len(w.birds)/2)]

        if len(self.values) >= 50:
            # Mark birds suspected to be nonflockers
            for i in range(0, len(w.birds)):
                bird_error = output[i]
                bird = w.birds[i]
                if bird_error > self.median_error*self.treshold_multiplier:
                    bird.marked = True
                    if type(bird) == faulty_bird.NonFlocker:
                        self.TP += 1
                    else:
                        self.FP += 1
                else:
                    bird.marked = False
                    if type(bird) == faulty_bird.NonFlocker:
                        self.FN += 1
                    else:
                        self.TN += 1

            # print TP and FP
            P = self.TP + self.FP
            N = self.TN + self.FN
            if P > 0 and N > 0:
                print(self.TP / P, self.FN / N, self.TP, self.FP, self.TN, self.FN)

    def draw(self, screen):
        screen.fill((0, 0, 0))

        distance = self.w/self.max_length

        # top = max(self.values)*1.01
        # bot = min(self.values)*0.99
        median_height = self.h*((5-(self.median_error*self.treshold_multiplier))/5)
        avg_height = self.h*((5-(self.avg_error*self.treshold_multiplier))/5)
        fixed_height = self.h*((5-(1))/5)
        pygame.draw.aaline(screen, (0, 255, 0), (0.0, median_height), (self.w, median_height))
        pygame.draw.aaline(screen, (0, 0, 255), (0.0, avg_height), (self.w, avg_height))
        pygame.draw.line(screen, (255, 255, 0), (0.0, fixed_height), (self.w, fixed_height))

        top = 5
        bot = 0
        color = (250, 250, 250)
        for tracked in range(0, self.good_count + self.bad_count):
            points = []
            for i in range(self.current_index, -1, -1):
                x = self.w - ((self.current_index-i) * distance)
                y = ((top-self.values[i][tracked]) / (top-bot)) * self.h
                points.append((x, y))

            for i in range(len(self.values)-1, self.current_index, -1):
                x = self.w - ((self.current_index+(100-i)) * distance)
                y = ((top - self.values[i][tracked]) / (top - bot)) * self.h
                points.append((x, y))

            if tracked >= self.good_count:
                color = (250, 0, 0)
            if len(points) > 1:
                pygame.draw.lines(screen, color, False, points)
