import intruder
from world import World
import world_configs
from data_analyzer import DataAnalyzer
from bird import Bird
import sys
import os
from datetime import datetime


layout = world_configs.HourGlass
intruder_type = intruder.NonFlocker


width = 1200
height = 900

good_count = 50
bad_count = 10
bird_count = good_count + bad_count

p_std = 5
v_std = 5

timesteps = 2000

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

        charter = DataAnalyzer(width, 10, 100, good_count, bad_count)

        for step in range(0, 2000):
            w.update(10)
            charter.track(w)
            error_time_bad[step] += charter.bad_error_sum/bad_count
            error_time_good[step] += charter.good_error_sum/good_count
            charter.bad_error_sum = 0.0
            charter.good_error_sum = 0.0

            distances = []

            for i in range(0, bird_count):
                bird = w.birds[i]
                is_bad = type(bird) != Bird
                distance = bird.time_since_target
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

            avg_t_since_t.append(sum(distances)/len(distances))

    print(simulation)
    print(sum(avg_t_since_t)/len(avg_t_since_t))


layout_string = str(layout.__name__).lower()
intruder_string = str(intruder_type.__name__).lower()


subfolder = layout_string + '/' + intruder_string + '/'
file_t = subfolder + "time.dat"
file_t_since_t = subfolder + "time_since_target.dat"

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

