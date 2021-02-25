import matplotlib.pyplot as plt

layout = 'hourglass'
intruder_type = 'nonflocker'


FPRs = []
TPRs = []

filename = layout + '/' + intruder_type + '/roc_5_0.02.dat'
# filename = layout + '/' + intruder_type + '/results_5_5.dat'



with open(filename, 'r') as f:
    line = f.readline()
    title = 'p_std, v_std = ' + line
    line = f.readline()
    line = f.readline()
    while line != '':
        values = line.split(',')
        FPRs.append(float(values[2].strip()))
        TPRs.append(float(values[1].strip()))
        line = f.readline()

plt.ylim((0, 1))
plt.plot(FPRs, TPRs, marker='o')
plt.title(title)
plt.show()