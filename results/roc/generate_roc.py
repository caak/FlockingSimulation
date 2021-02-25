import layouts
from tracer import Tracer
import intruder
import os

width = 1200
height = 900

good_count = 50
bad_count = 10
bird_count = good_count + bad_count

threshold = 0

layout = layouts.HourGlass
intruder_type = intruder.NonFlocker

p_std = 5
v_std = 0.2

print(p_std, v_std)

output = str(p_std) + ', ' + str(v_std)
output += '\nthreshold, TPR, FPR\n'


for simulation in range(0, 50):
    FPR = []
    TPR = []

    bad_sums = []
    good_sums = []
    for i in range(0, 3):
        w = layout(width, height, good_count, bad_count, p_std=p_std, v_std=v_std, intruder_type=intruder_type)

        charter = Tracer(width, 10, 100, good_count, bad_count)

        charter.threshold_multiplier = threshold

        for i in range(0, 1500):
            w.update(1)
            charter.track(w)
        P = charter.TP + charter.FN
        N = charter.TN + charter.FP
        FPR.append(charter.FP / N)
        TPR.append(charter.TP / P)

    avg_FPR = sum(FPR)/len(FPR)
    avg_TPR = sum(TPR)/len(TPR)


    output += str(threshold) + ', ' + str(avg_TPR) + ', ' + str(avg_FPR) + '\n'

    print(simulation)

    if avg_FPR == 0.0:
        print('no point continuing')
        break
    threshold += 0.2

layout_string = str(layout.__name__).lower()
intruder_string = str(intruder_type.__name__).lower()

subfolder = layout_string + '/' + intruder_string + '/'
file_name = subfolder + "roc_5_0.2.dat"

if not os.path.isdir(layout_string):
    os.mkdir(layout_string)

if not os.path.isdir(subfolder):
    os.mkdir(subfolder)


with open(file_name, 'w') as f:
    f.write(output)
