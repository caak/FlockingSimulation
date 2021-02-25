import layouts
from tracer import Tracer
from bird import Bird
import pygame
import time
import numpy as np
from timed_world import TimedWorld

iteration_count = 500

width = 1200
height = 900

good_count = 50
bad_count = 10
bird_count = good_count + bad_count

threshold = 0

hourglass = layouts.HourGlass(width, height, good_count, bad_count)
w = TimedWorld(hourglass.width, hourglass.height)
w.birds = hourglass.birds
w.targets = hourglass.targets
w.p_stds = hourglass.p_stds
w.v_stds = hourglass.v_stds


charter = Tracer(width, 10, 100, good_count, bad_count)

charter.threshold_multiplier = threshold

clock = pygame.time.Clock()
current_t = time.thread_time_ns()

update_ts = np.zeros(iteration_count)
chart_ts = np.zeros(iteration_count)
ts = np.zeros((iteration_count, 6))

# Do a first step without time tracking, to initialize everything
w.update(10)
charter.track(w)


for i in range(0, iteration_count):
    ts[i][:] = w.update(10)
    update_ts[i] = time.thread_time_ns() - current_t
    charter.track(w)
    chart_ts[i] = time.thread_time_ns() - current_t - update_ts[i]
    new_t = time.thread_time_ns()
    total_duration = new_t - current_t
    current_t = new_t


update_t = sum(update_ts)/len(update_ts)
chart_t = sum(chart_ts)/len(chart_ts)
total_t = update_t + chart_t
times = np.divide(ts.sum(axis=0), iteration_count)

print(update_t)

print('update_ts, chart_ts')
print(update_t/total_t, chart_t/total_t)

print('t_distances, t_update_bird, t_update_vs, t_update_ps')
print(np.divide(times, update_t))

# sigma_update_t = sum(np.square(np.subtract(update_ts, update_t)))/2000
# sigma_chart_t = sum(np.square(np.subtract(chart_ts, chart_t)))/2000
#
# print(np.sqrt(sigma_update_t), np.sqrt(sigma_chart_t))

print((Bird.total_duration/iteration_count)/update_t)