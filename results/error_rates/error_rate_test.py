import sys
sys.path.append("/home/simon/Desktop/flocker/flocking-simulation")
# sys.path.append('/')
import layouts
from tracer import Tracer
import sys
import os
import intruder
import numpy as np
import pygame

width = 1200
height = 900

layout = layouts.HourGlass
intruder_type = intruder.NonFlocker

step_count = 2000

good_count = 50
bad_count = 10
bird_count = good_count + bad_count

threshold = 0

p_std = 0
v_std = float(sys.argv[1]) * float(sys.argv[2])

goods = []
bads = []
ratios = []
p_stds = []
avg_distances = []


for simulation in range(0, 21):
    FPR = []
    TPR = []

    bad_sums = []
    good_sums = []
    n = good_count + bad_count
    distances = np.zeros((n, n))
    for i in range(0, 10):
        w = layout(width, height, good_count, bad_count, p_std, v_std, intruder_type=intruder_type)
        w.positions = [pygame.Vector2(0, 0)] * n

        charter = Tracer(width, 10, 100, good_count, bad_count)


        for step in range(0, step_count):
            w.update(1)
            charter.track(w)
            distances = np.add(distances, w.distances)
        P = charter.TP + charter.FN
        N = charter.TN + charter.FP
        bad_sums.append(charter.bad_error_sum/P)
        good_sums.append(charter.good_error_sum/N)

    avg_bad_error = sum(bad_sums)/len(bad_sums)
    avg_good_error = sum(good_sums)/len(good_sums)

    avg_distance = np.sum(distances)/(10*step_count*n*n)

    goods.append(avg_good_error)
    bads.append(avg_bad_error)
    ratios.append(avg_good_error/avg_bad_error)
    p_stds.append(p_std)
    avg_distances.append(avg_distance)

    print(v_std, p_std, avg_good_error, avg_bad_error, avg_distance)

    p_std += 0.4



subfolder = sys.argv[3]
filename = subfolder + "/results_" + '%.5f' %v_std

layout_string = str(layout.__name__).lower()
intruder_string = str(intruder_type.__name__).lower()

if not os.path.isdir(subfolder):
    os.mkdir(subfolder)


with open(filename, "w") as f:
    txt = "v_std: {vstd:.5f}, layout: {layout}, intruder: {intruder}, stepcount: {step_count} \n"
    f.write(txt.format(vstd=v_std, layout=layout_string, intruder=intruder_string, step_count=step_count))
    f.write('p_std, ratio\n')
    for i in range(0, len(ratios)):
        f.write(str(p_stds[i])+','+str(ratios[i]) +',' + str(avg_distances[i]) + '\n')
