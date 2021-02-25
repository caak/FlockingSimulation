import matplotlib.pyplot as plt
import os

print(os.listdir('/'))


import numpy as np

layout = 'hourglass'
intruder = 'nonflocker'

folder = layout + '/' + intruder


xs = []
goods = []
bads = []

step = 0
with open(folder + "/time.dat", 'r') as f:
    line = f.readline()
    while line[0] != 'p':

        if step > 1:
            xs.append(step)
            values = line.split(',')
            goods.append(float(values[0]))
            bads.append(float(values[1]))
        step += 1
        line = f.readline()

plt.rcParams.update({'font.size': 22})
plt.scatter(xs, goods, label='normal drones', marker='x')
plt.scatter(xs, bads, label='intruders', marker='o')
# plt.ylim((2, 6))
plt.title('Residual over time')
plt.ylabel("Residual")
plt.xlabel("Time")
plt.legend()

fig = plt.figure()

bad_x = []
bad_y = []

good_x = []
good_y = []

with open(folder + "/time_since_target.dat", 'r') as f:
    f.readline()
    line = f.readline()
    line = f.readline()
    while line[0:4] != 'good':
        values = line.split(',')
        print(values)
        bad_x.append(int(values[0]))
        bad_y.append(float(values[1]))
        line = f.readline()
    line = f.readline()
    while len(line) != 0:
        values = line.split(',')
        good_x.append(int(values[0]))
        good_y.append(float(values[1]))
        line = f.readline()

# plt.ylim((2, 6))
# plt.xlim((0, 100))
# plt.scatter(bad_x, bad_y, marker='x')
# plt.scatter(good_x, good_y, marker='o')

plt.scatter(bad_x, bad_y, label='intruders', marker='x')
plt.scatter(good_x, good_y, label='normal drones', marker='o')
plt.title('Residual at time since last target')
plt.ylabel("Residual")
plt.xlabel("Time since target")
plt.legend()

plt.show()
