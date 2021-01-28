from world import World
import world_configs
from data_analyzer import DataAnalyzer
from bird import Bird

width = 1200
height = 900

good_count = 50
bad_count = 10
bird_count = good_count + bad_count

threshold = 0


output = 'threshold, TPR, FPR\n'


for simulation in range(0, 20):
    FPR = []
    TPR = []

    bad_sums = []
    good_sums = []
    for i in range(0, 1):
        w = world_configs.HourGlass(width, height, good_count, bad_count, p_std=1, v_std=1)

        charter = DataAnalyzer(width, 10, 100, good_count, bad_count)

        charter.threshold_multiplier = threshold

        for i in range(0, 2000):
            w.update(10)
            charter.track(w)
        P = charter.TP + charter.FN
        N = charter.TN + charter.FP
        FPR.append(charter.FP / N)
        TPR.append(charter.TP / P)
        bad_sums.append(charter.bad_error_sum/P)
        good_sums.append(charter.good_error_sum/N)

    avg_FPR = sum(FPR)/len(FPR)
    avg_TPR = sum(TPR)/len(TPR)

    avg_bad_error = sum(bad_sums)/len(bad_sums)
    avg_good_error = sum(good_sums)/len(good_sums)


    output += str(threshold) + ', ' + str(avg_TPR) + ', ' + str(avg_FPR) + '\n'

    print(simulation)

    if avg_FPR == 0.0:
        print('no point continuing')
        break
    threshold += 0.2

with open('results/roc/hourglass/non_flocker/results_1_1.dat', 'w') as f:
    f.write(output)