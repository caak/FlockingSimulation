import matplotlib.pyplot as plt

FPRs = []
TPRs = []

with open('hourglass/non_flocker/results_1_1.dat', 'r') as f:
    line = f.readline()
    line = f.readline()
    while line != '':
        values = line.split(',')
        FPRs.append(float(values[2].strip()))
        TPRs.append(float(values[1].strip()))
        line = f.readline()

plt.plot(FPRs, TPRs)
plt.show()