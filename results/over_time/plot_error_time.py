import matplotlib.pyplot as plt
import os

print(os.listdir('/'))

def read_data_file(filepath):
    xs = []
    goods = []
    bads = []

    step = 0
    step_size = 20
    # line = f.readline()
    line = 'tmep'
    with open(filepath, 'r') as f:
        while line[0] != 'p':
            line = f.readline()
            if step > 1:
                xs.append(step)
                avg_good = 0.0
                avg_bad = 0.0
                for i in range(0, step_size):
                    if line[0] == 'p':
                        break
                    values = line.split(',')
                    avg_bad += float(values[1])
                    avg_good += float(values[0])
                    line = f.readline()

                goods.append(avg_good / step_size)
                bads.append(avg_bad / step_size)

            step += step_size

    goods.pop()
    bads.pop()
    xs.pop()

    return xs, goods, bads

layout = 'hourglass'
intruder = 'nonflocker'

folder = layout + '/' + intruder

non_flocker_xs, non_flocker_goods, non_flocker_bads = read_data_file(folder + '/time.dat')



plt.rcParams.update({'font.size': 22})
fig, (ax1, ax2) = plt.subplots(1, 2)
# ax1.set_ylim((0.005, 0.02))
# ax2.set_ylim((0.005, 0.02))
ax1.plot(non_flocker_xs, non_flocker_goods, label='normal drones', linewidth=5)
ax1.plot(non_flocker_xs, non_flocker_bads, label='intruders', linestyle='--')

# ax1.title('Residual over time')
# ax1.ylabel("Residual")
# ax1.xlabel("Time")
# ax1.set_ylim(bottom=2, top=6)
ax1.set(xlabel='Time', ylabel='Residual')
ax1.set_title('Nonflocker')
ax1.legend()

layout = 'hourglass'
intruder = 'follower'

folder = layout + '/' + intruder

non_flocker_xs, non_flocker_goods, non_flocker_bads = read_data_file(folder + '/time.dat')



ax1.set_ylim((0.04, 0.08))
ax2.set_ylim((0.04, 0.08))
ax2.plot(non_flocker_xs, non_flocker_goods, label='normal drones', linewidth=5)
ax2.plot(non_flocker_xs, non_flocker_bads, label='intruders', linestyle='--')

# ax1.title('Residual over time')
# ax1.ylabel("Residual")
# ax1.xlabel("Time")
# ax1.set_ylim(bottom=2, top=6)
ax2.set(xlabel='Time', ylabel='Residual')
# ax1.set_title('Residual over time')
ax2.set_title('Follower')

ax1.legend()


plt.ylabel("Residual")
plt.xlabel("Time")
plt.legend()
fig.suptitle('Residual over Time')

plt.show()
