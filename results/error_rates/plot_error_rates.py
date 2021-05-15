import matplotlib.pyplot as plt

import os

import numpy as np

plt.rcParams.update({'font.size': 22})

#15:35 - 16:10

# run = '25-01-2021_15-02-10'

# run = '25-01-2021_15-35-51'
# run = '29-01-2021_21-58-34'
# run = '14-02-2021_14-10-01'
# run = '14-02-2021_16-15-52'
# run = '14-05-2021_17-56-56'
# run = '14-05-2021_18-12-37'
# run = '14-05-2021_18-28-07'
# run = '14-05-2021_18-43-12'
run = '14-05-2021_18-55-36'
dir = run

v_std_count = len(os.listdir(run))

z = np.zeros((21,21))


for i in range(0, 21):
    v_std = (i * 0.0015)
    v_std_str = '%.5f' % v_std
    with open(dir + "/results_" + str(v_std_str), 'r') as f:
        f.readline()
        f.readline()
        line = f.readline()
        j = 0
        while line != '':
            values = line.split(',')
            p_std = float(values[0])
            ratio = float(values[1])
            z[i, j] = ratio
            j += 1
            line = f.readline()


print(v_std_count, j, p_std, v_std_str)
# generate 2 2d grids for the x & y bounds
x, y = np.meshgrid(np.linspace(0, p_std, j), np.linspace(0, v_std, v_std_count))

# z = (1 - x / 2. + x ** 5 + y ** 3) * np.exp(-x ** 2 - y ** 2)
# x and y are bounds, so z should be the value *inside* those bounds.
# Therefore, remove the last value from the z array.
# z = z[:-1, :-1]
z_min, z_max = -np.abs(z).max(), np.abs(z).max()


plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
plt.rc('ytick', labelsize=12)    # fontsize of the tick labels

fig = plt.figure()
ax = fig.gca(projection='3d')
# fig, ax = plt.subplots()

c = ax.plot_surface(x, y, z, cmap='Greys', vmin=0, vmax=1)
# c = ax.pcolormesh(x, y, z, cmap='Greys', vmin=0, vmax=1)
ax.set_title('\"normal error\" / \"intruder error\"')
# set the limits of the plot to the limits of the data
# ax.axis([0, 11, 0, 2])
cbar = fig.colorbar(c, ax=ax, fraction=0.046, pad=0.04)
cbar.ax.tick_params(labelsize=20)
ax.set_xlabel('position error', labelpad=10)
ax.set_ylabel('velocity error', labelpad=10)
ax.set_zlabel('avg normal error / avg intruder error', labelpad=10)

plt.show()
