import intruder
import layouts
from tracer import Tracer
import numpy as np
import pygame

width = 1200
height = 900

good_count = 50
bad_count = 10
bird_count = good_count + bad_count

p_std = 2
v_std = 0.02

timesteps = 2000

error_time_bad = [0]*timesteps
error_time_good = [0]*timesteps

bad_scatter = {}
good_scatter = {}

avg_t_since_t = []

layouts = [layouts.HourGlass, layouts.Circle, layouts.Merge]
layout_time = [2000, 2000, 800]

intruders = [intruder.NonFlocker, intruder.Follower]

intruder_type = intruder.NonFlocker

FPR = np.zeros((3, 2))
TPR = np.zeros((3, 2))
for i in range(0, len(layouts)):
    layout = layouts[i]
    for j in range(0, len(intruders)):
        intruder_type = intruders[j]
        TPRs = []
        FPRs = []
        for k in range(0, 3):
            w = layout(width, height, good_count, bad_count, p_std, v_std, intruder_type)
            w.positions = [pygame.Vector2(0, 0)] * bird_count

            charter = Tracer(width, 10, 100, good_count, bad_count)

            for step in range(0, layout_time[i]):
                w.update(1)
                charter.track(w)
            P = charter.TP + charter.FN
            N = charter.TN + charter.FP
            FPRs.append(charter.FP / N)
            TPRs.append(charter.TP / P)
        TPR[i][j] = sum(TPRs)/len(TPRs)
        FPR[i][j] = sum(FPRs)/len(FPRs)
        print(i, j)

for j in range(0, len(intruders)):
    print('\\multirow{2}{5em}{Nonflocker} & TPR &', end='')
    for i in range(0, len(layouts)):
        print("{:.4f}".format(TPR[i][j]), end=' & ')
    print('\n& FPR &', end='')
    for i in range(0, len(layouts)):
        print("{:.4f}".format(FPR[i][j]), end=' & ')
    print('\n\\hline')
