import layouts
import pygame
import intruder
from bird import Bird
import matplotlib.pyplot as plt
import random


def calculate_neighbor_avoidance(self, n, world):
    bird = world.birds[self.neighbours[n]]
    distance = (self.p - bird.p) + Bird.error_vector(self.p_std)
    if distance.length_squared() == 0:
        # This case helps break birds apart, stuck in the same position
        distance = pygame.Vector2((random.randint(0, 1) - 0.5) * 0.1, (random.randint(0, 1) - 0.5) * 0.1)
    else:
        distance = distance.normalize() * (1 / distance.length())
    return distance


normal_bird_count = 50
bad_bird_count = 1

w = layouts.HourGlass(1200, 700, normal_bird_count)
interval = normal_bird_count * 50.0 / bad_bird_count
for i in range(0, bad_bird_count):
    w.birds.append(intruder.Follower(200 + (i % 2), 490 + (interval * i), len(w.birds), 10, 1))

w.birds[50].p_std

x = []
y_good = []
y_bad = []

for i in range(0, 1000):
    x.append(i)
    w.calculate_distances()
    measurements = {}
    for bird in w.birds:
        bird.update_neighbours(w)
        bird.update_measurements(w)

    for bird in w.birds:
        attraction = pygame.Vector2(0, 0)
        avoidance = pygame.Vector2(0, 0)
        alignment = pygame.Vector2(0, 0)

        for n in bird.neighbours:
            neighbor = w.birds[n]

            distance = neighbor.p - bird.p + neighbor.error_vector(neighbor.p_std)
            velocity = neighbor.v
            for nn in range(0, len(neighbor.neighbours)):
                if neighbor.neighbours[nn] == bird.id:
                    distance = neighbor.p_measurements[nn]
                    velocity = neighbor.v_measurements[nn]
                    break

            predicted_v = distance * Bird.attraction_weight / len(neighbor.neighbours)
            predicted_v += velocity * Bird.alignment_weight / len(neighbor.neighbours)
            predicted_v += (-distance).normalize() / distance.length() * Bird.avoidance_weight

            target = (w.targets[bird.current_target] - bird.p)
            if target.length_squared() > 0:
                target = target.normalize()
            predicted_v += target * Bird.target_weight
            predicted_v *= Bird.turn_rate_factor
            predicted_v += bird.v

            if predicted_v.length_squared() > Bird.max_speed_squared:
                predicted_v *= Bird.max_speed_squared / predicted_v.length_squared()



            if bird not in measurements.keys():
                measurements[bird] = []
            measurements[bird].append((neighbor, predicted_v))

    for bird in w.birds:
        bird.update_v(w)

    # Bird.print_bird_stats() # this prints info on how much each rule matters

    for bird in w.birds:
        bird.update_p(10)

    errors_good = []
    errors_bad = []
    for bird in measurements.keys():
        # bird = w.birds[id]
        real = bird.v
        error = pygame.Vector2(0, 0)
        for (neighbor, prediction) in measurements[bird]:
            error += prediction-real

        avg_error = error.length() / len(measurements[bird])

        if bird.id == 5:
            errors_good.append(avg_error)
        elif bird.id == 50:
            errors_bad.append(avg_error)

    y_bad.append(sum(errors_bad) / len(errors_bad))

    y_good.append(sum(errors_good)/len(errors_good))

plt.plot(x, y_bad, label='Bad measurements drone')

plt.plot(x, y_good, label='normal drone')


plt.legend()

plt.ylabel('error')
plt.title('average errors for different classes of noisy birds')
plt.show()
