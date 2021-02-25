import layouts
from tracer import Tracer
import time
import numpy as np

iteration_count = 500

width = 1200
height = 900

good_count = 50
bad_count = 10
bird_count = good_count + bad_count

threshold = 1

w = layouts.HourGlass(width, height, good_count, bad_count)

charter = Tracer(width, 10, 100, good_count, bad_count)

charter.threshold_multiplier = threshold

current_t = time.thread_time_ns()

update_ts = np.zeros(iteration_count)
chart_ts = np.zeros(iteration_count)
ts = np.zeros((iteration_count, 6))

# Do a first step without time tracking, to initialize everything
w.update(10)
charter.track(w)


for i in range(0, iteration_count):
    w.update(10)
    update_ts[i] = time.thread_time_ns() - current_t
    ts[i][:] = charter.track(w)
    chart_ts[i] = time.thread_time_ns() - current_t - update_ts[i]
    new_t = time.thread_time_ns()
    total_duration = new_t - current_t
    current_t = new_t


update_t = sum(update_ts)/len(update_ts)
chart_t = sum(chart_ts)/len(chart_ts)
total_t = update_t + chart_t

print('update_ts, chart_ts')
print(update_t/total_t, chart_t/total_t)

times = np.divide(ts.sum(axis=0), iteration_count)

print(np.divide(times, chart_t))

# sigma_update_t = sum(np.square(np.subtract(update_ts, update_t)))/2000
# sigma_chart_t = sum(np.square(np.subtract(chart_ts, chart_t)))/2000
#
# print(np.sqrt(sigma_update_t), np.sqrt(sigma_chart_t))
