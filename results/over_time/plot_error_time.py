import matplotlib.pyplot as plt
import os

print(os.listdir('./'))


import numpy as np

layout = 'hourglass'
intruder = 'non_flocker'

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


plt.plot(xs, goods)
plt.plot(xs, bads)

plt.figure()

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

plt.ylim((0, 10))
plt.xlim((0, 100))
plt.scatter(bad_x, bad_y, color='red')
plt.scatter(good_x, good_y, color='black')

plt.show()
