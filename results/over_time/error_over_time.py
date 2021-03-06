import intruder
import layouts
from tracer import Tracer
from bird import Bird
import pygame
import os

layout = layouts.HourGlass
intruder_type = intruder.Follower


width = 1200
height = 900

good_count = 50
bad_count = 10
bird_count = good_count + bad_count

p_std = 5.0
v_std = 0.1

timesteps = 5000

error_time_bad = [0]*timesteps
error_time_good = [0]*timesteps

bad_scatter = {}
good_scatter = {}

avg_t_since_t = []

for simulation in range(0, 10):
    FPR = []
    TPR = []

    bad_sums = []
    good_sums = []
    for i in range(0, 1):
        w = layout(width, height, good_count, bad_count, p_std, v_std, intruder_type)
        w.positions = [pygame.Vector2(0, 0)] * bird_count

        charter = Tracer(width, 10, 100, good_count, bad_count)

        for step in range(0, timesteps):
            w.update(1)
            charter.track(w)

            # if step < 50:
            #     continue

            error_time_bad[step] += charter.bad_error_sum/bad_count
            error_time_good[step] += charter.good_error_sum/good_count

            distances = []

            for i in range(0, bird_count):
                bird = w.birds[i]
                is_bad = type(bird) != Bird
                distance = bird.time_since_target
                # distance = int(bird.distance_to_target)
                error = charter.errors[charter.current_index][i]
                if is_bad:
                    if distance not in bad_scatter.keys():
                        bad_scatter[distance] = []
                    bad_scatter[distance].append(error)
                else:
                    distances.append(distance)
                    if distance not in good_scatter.keys():
                        good_scatter[distance] = []
                    good_scatter[distance].append(error)

    print(simulation)


layout_string = str(layout.__name__).lower()
intruder_string = str(intruder_type.__name__).lower()


subfolder = layout_string + '/' + intruder_string + '/'
file_t = subfolder + "time.dat"
file_t_since_t = subfolder + "time_since_target.dat"

print(subfolder)

if not os.path.isdir(subfolder):
    os.mkdir(subfolder)


with open(file_t, "w") as f:
    txt = "p_std: {pstd:.2f}, v_std: {vstd:.2f}"
    f.write(str(error_time_good[0]/10) + ', ' + str(error_time_bad[0]/10))
    for i in range(1, timesteps):
        f.write('\n')
        f.write(str(error_time_good[i]/10) + ', ' + str(error_time_bad[i]/10))

    f.write('\n')
    f.write(txt.format(pstd=p_std, vstd=v_std))

with open(file_t_since_t, "w") as f:
    txt = "p_std: {pstd:.2f}, v_std: {vstd:.2f}"
    f.write(txt.format(pstd=p_std, vstd=v_std))
    f.write('\n')
    f.write('bad:\n')
    for t, values in bad_scatter.items():
        f.write(str(t) + ', ' + str(sum(values)/len(values)))
        f.write('\n')

    f.write('good:\n')
    for t, values in good_scatter.items():
        f.write(str(t) + ', ' + str(sum(values)/len(values)))
        f.write('\n')

