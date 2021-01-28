import sys
sys.path.append('/home/simon/Desktop/flocker/flocking-simulation')
import world_configs
from data_analyzer import DataAnalyzer
import sys
import os
import intruder

width = 1200
height = 900

good_count = 50
bad_count = 10
bird_count = good_count + bad_count

threshold = 0

p_std = 0
v_std = float(sys.argv[1]) * float(sys.argv[2])

goods = []
bads = []
ratios = []


for simulation in range(0, 21):
    FPR = []
    TPR = []

    bad_sums = []
    good_sums = []
    for i in range(0, 3):
        w = world_configs.HourGlass(width, height, good_count, bad_count, p_std, v_std, intruder.NonFlocker)

        charter = DataAnalyzer(width, 10, 100, good_count, bad_count)

        for step in range(0, 2000):
            w.update(10)
            charter.track(w)
        P = charter.TP + charter.FN
        N = charter.TN + charter.FP
        bad_sums.append(charter.bad_error_sum/P)
        good_sums.append(charter.good_error_sum/N)

    avg_bad_error = sum(bad_sums)/len(bad_sums)
    avg_good_error = sum(good_sums)/len(good_sums)

    goods.append(avg_good_error)
    bads.append(avg_bad_error)
    ratios.append(avg_good_error/avg_bad_error)

    print(v_std, p_std, avg_good_error, avg_bad_error)

    p_std += 1



subfolder = sys.argv[3]
filename = subfolder + "/results_" + str(v_std)

if not os.path.isdir(subfolder):
    os.mkdir(subfolder)


with open(filename, "w") as f:
    f.write(str(ratios[0]))
    for i in range(1, len(ratios)):
        f.write(',')
        f.write(str(ratios[i]))

    f.write('\n')
    txt = "p_std: {pstd:.2f}, v_std: {vstd:.2f}"
    f.write(txt.format(pstd=p_std, vstd=v_std))
