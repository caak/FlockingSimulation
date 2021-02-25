import pygame
from bird import Bird
import numpy as np
import intruder
import time


class Tracer:
    def __init__(self, w, h, tracking_length, good_count, bad_count):
        self.errors = []
        self.avg_errors = []
        self.max_length = tracking_length
        self.current_index = -1

        self.w = w
        self.h = h

        self.good_count = good_count
        self.bad_count = bad_count

        self.avg_error = 0.0
        self.median_error = 0.0

        self.threshold_multiplier = 2.0

        self.FP = 0
        self.TP = 0
        self.FN = 0
        self.TN = 0

        self.good_error_sum = 0.0
        self.bad_error_sum = 0.0

        self.max_error = 0.0

    def reset_confusion_matrix(self):
        self.FP = 0
        self.TP = 0
        self.FN = 0
        self.TN = 0

    def track(self, w):
        # self.good_error_sum = 0.0
        # self.bad_error_sum = 0.0

        self.current_index += 1
        if self.current_index == self.max_length:
            self.current_index = 0

        errors = []
        avg_errors = []


        for t in range(0, self.good_count + self.bad_count):
            current_t = time.thread_time_ns()
            bird = w.birds[t]

            ps, vs, v2s = self.infer_measurements(w, bird)
            target = self.infer_target(w, bird)


            prediction = Bird.flock(ps, vs, target, bird.old_v)

            avg_v_observed = pygame.Vector2(0,0)
            for v in v2s:
                avg_v_observed += v

            avg_v_observed /= len(v2s)

            error = (prediction-avg_v_observed).length()

            errors.append(error)

            avg_errors.append(self.calculate_running_avg(t, error))


        if len(self.errors) < self.max_length:
            self.errors.append(errors)
        else:
            self.errors[self.current_index] = errors

        if len(self.avg_errors) < self.max_length:
            self.avg_errors.append(avg_errors)
        else:
            self.avg_errors[self.current_index] = avg_errors


        self.avg_error = 0
        for error in errors:
            self.avg_error += error
        self.avg_error /= len(w.birds)

        self.median_error = sorted(avg_errors)[int(len(w.birds)/2)]

        self.mark_suspicious_birds(w)


    def draw(self, screen):
        screen.fill((0, 0, 0))

        distance = self.w/self.max_length

        # top = max(self.values)*1.01
        # bot = min(self.values)*0.99
        top = self.max_error
        if top == 0.0:
            top = 1
        bot = 0
        median_height = self.h*((top-(self.median_error*self.threshold_multiplier))/top)
        avg_height = self.h*((top-(self.avg_error*self.threshold_multiplier))/top)
        fixed_height = self.h*((top-0.005)/top)
        pygame.draw.aaline(screen, (0, 255, 0), (0.0, median_height), (self.w, median_height))
        pygame.draw.aaline(screen, (0, 0, 255), (0.0, avg_height), (self.w, avg_height))
        pygame.draw.line(screen, (255, 255, 0), (0.0, fixed_height), (self.w, fixed_height))

        color = (250, 250, 250)
        if len(self.avg_errors) < 50:
            return
        for tracked in range(0, self.good_count + self.bad_count):
            points = []
            for i in range(self.current_index, -1, -1):
                x = self.w - ((self.current_index-i) * distance)

                y = ((top - self.avg_errors[i][tracked]) / (top - bot)) * self.h
                points.append((x, y))

            for i in range(len(self.avg_errors) - 1, self.current_index, -1):
                x = self.w - ((self.current_index+(100-i)) * distance)
                y = ((top - self.avg_errors[i][tracked]) / (top - bot)) * self.h
                points.append((x, y))

            if tracked >= self.good_count:
                color = (250, 0, 0)
            if len(points) > 1:
                pygame.draw.lines(screen, color, False, points)

    def infer_measurements(self, w, bird):
        ps = [0] * Bird.neighborhood_size
        vs = [0] * Bird.neighborhood_size
        v2s = [0] * Bird.neighborhood_size
        for i in range(0, len(bird.neighbours)):
            n = w.birds[bird.neighbours[i]]
            found = False
            for j in range(0, len(n.neighbours)):
                if bird.id == n.neighbours[j]:
                    ps[i] = -n.p_measurements[j]
                    found = True

            if not found:
                distance = n.old_p - bird.old_p + pygame.Vector2(w.p_errors[n.id][bird.id * 2],w.p_errors[n.id][bird.id * 2 + 1])
                ps[i] = distance

            vs[i] = n.old_v + pygame.Vector2(w.v_errors[n.id][bird.id * 2], w.v_errors[n.id][bird.id * 2 + 1])
            v2s[i] = bird.v + pygame.Vector2(w.v_errors[n.id][bird.id * 2], w.v_errors[n.id][bird.id * 2 + 1])

        return ps, vs, v2s

    def infer_target(self, w, bird):
        if len(bird.target_sequence) > 0:
            target = (bird.target_sequence[bird.current_target] - bird.old_p)
        else:
            target = pygame.Vector2(0, 0)
        if target.length_squared() > 0:
            target = target.normalize()
        target *= Bird.target_weight
        return target

    def calculate_running_avg(self, bird, error):
        average_length = 50
        if len(self.errors) >= average_length:
            index = self.current_index-1
            for i in range(0, average_length-1):
                if index < 0:
                    index = self.max_length - 1
                error += self.errors[index][bird]
                index -= 1
            error = error / average_length
        if error > self.max_error and len(self.avg_errors) >= 50:
            self.max_error = error
        return error

    def mark_suspicious_birds(self, w):
        if len(self.avg_errors) >= 0:
            # Mark birds suspected to be nonflockers
            for i in range(0, len(w.birds)):
                bird_error = self.avg_errors[self.current_index][i]
                bird = w.birds[i]

                is_intruder = type(bird) != Bird

                if is_intruder:
                    self.bad_error_sum += self.errors[self.current_index][i]
                else:
                    self.good_error_sum += self.errors[self.current_index][i]

                if bird_error > self.median_error * self.threshold_multiplier:
                    bird.marked = True
                    if is_intruder: # and bird.p.x < record_limit:
                        self.TP += 1
                    else:
                        self.FP += 1
                else:
                    bird.marked = False
                    if is_intruder: # and bird.p.x < record_limit:
                        self.FN += 1
                    else:
                        self.TN += 1
