import matplotlib.pyplot as plt

import os

import numpy as np

#15:35 - 16:10

# run = '25-01-2021_15-02-10'

run = '25-01-2021_15-35-51'
dir =  run

z = np.zeros((21,21))


for i in range(0, 21):
    v_std = round(i*0.1, 4)
    with open(dir + "/results_" + str(v_std), 'r') as f:
        values = f.readline().split(',')
        for p_std in range(0, len(values)):
            z[i, p_std] = float(values[p_std])


# generate 2 2d grids for the x & y bounds
x, y = np.meshgrid(np.linspace(0, 20, 21), np.linspace(0, 2, 21))

# z = (1 - x / 2. + x ** 5 + y ** 3) * np.exp(-x ** 2 - y ** 2)
# x and y are bounds, so z should be the value *inside* those bounds.
# Therefore, remove the last value from the z array.
# z = z[:-1, :-1]
z_min, z_max = -np.abs(z).max(), np.abs(z).max()


fig = plt.figure()
ax = fig.gca(projection='3d')
# fig, ax = plt.subplots()

c = ax.plot_surface(x, y, z, cmap='Greys', vmin=0, vmax=1)
# c = ax.pcolormesh(x, y, z, cmap='Greys', vmin=0, vmax=1)
ax.set_title('\"normal error\" / \"intruder error\"')
# set the limits of the plot to the limits of the data
# ax.axis([0, 11, 0, 2])
fig.colorbar(c, ax=ax)
ax.set_xlabel('position error')
ax.set_ylabel('velocity error')

plt.show()
