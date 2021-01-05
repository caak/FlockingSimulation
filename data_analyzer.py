import pygame
from bird import Bird
import numpy as np
import faulty_bird

class DataAnalyzer:
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

    def reset_confusion_matrix(self):
        self.FP = 0
        self.TP = 0
        self.FN = 0
        self.TN = 0

    # update and add current errors + avg_errors + avg_error + median_error
    def track(self, w):
        self.current_index += 1
        if self.current_index == self.max_length:
            self.current_index = 0

        errors = []
        avg_errors = []


        for t in range(0, self.good_count + self.bad_count):
            bird = w.birds[t]

            ps, vs = self.infer_measurements(w, bird)
            target = self.infer_target(w, bird)

            prediction = Bird.flock(ps, vs, target, bird.old_v)

            error = (prediction-bird.v).length()
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
        median_height = self.h*((5-(self.median_error*self.threshold_multiplier))/5)
        avg_height = self.h*((5-(self.avg_error*self.threshold_multiplier))/5)
        fixed_height = self.h*((5-(1))/5)
        pygame.draw.aaline(screen, (0, 255, 0), (0.0, median_height), (self.w, median_height))
        pygame.draw.aaline(screen, (0, 0, 255), (0.0, avg_height), (self.w, avg_height))
        pygame.draw.line(screen, (255, 255, 0), (0.0, fixed_height), (self.w, fixed_height))

        top = 5
        bot = 0
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
        ps = []
        vs = []
        for i in bird.neighbours:
            n = w.birds[i]
            found = False
            for j in range(0, len(n.neighbours)):
                if bird.id == n.neighbours[j]:
                    ps.append(-n.p_measurements[j])
                    vs.append(n.old_v + bird.error_vector(n.v_std))
                    found = True

            if not found:
                distance = n.old_p - bird.old_p + Bird.error_vector(n.p_std)
                velocity = n.old_v + Bird.error_vector(n.v_std)
                ps.append(distance)
                vs.append(velocity)

        return ps, vs

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
        average_length = 10
        if len(self.errors) >= average_length:
            index = self.current_index-1
            for i in range(0, average_length-1):
                if index < 0:
                    index = self.max_length - 1
                error += self.errors[index][bird]
                index -= 1
            error = error / average_length

        return error

    def mark_suspicious_birds(self, w):
        if len(self.avg_errors) >= 50:
            # Mark birds suspected to be nonflockers
            for i in range(0, len(w.birds)):
                bird_error = self.avg_errors[self.current_index][i]
                bird = w.birds[i]
                record_limit = 600
                if bird_error > self.median_error * self.threshold_multiplier:
                    bird.marked = True
                    if type(bird) == faulty_bird.NonFlocker: # and bird.p.x < record_limit:
                        self.TP += 1
                    else:
                        self.FP += 1
                else:
                    bird.marked = False
                    if type(bird) == faulty_bird.NonFlocker: # and bird.p.x < record_limit:
                        self.FN += 1
                    else:
                        self.TN += 1
