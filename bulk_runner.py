from world import World
import world_configs
from data_analyzer import DataAnalyzer
from bird import Bird

width = 1200
height = 900

good_count = 50
bad_count = 10
bird_count = good_count + bad_count

threshold = 1

for simulation in range(0, 30):
    w = world_configs.Merge(width, height, good_count, bad_count)

    charter = DataAnalyzer(width, 10, 100, good_count, bad_count)
    if simulation < 10:
        threshold += 0.1
    else:
        threshold += 0.2

    charter.threshold_multiplier = threshold

    for i in range(0, 560):
        w.update(10)
        charter.track(w)
    P = charter.TP + charter.FN
    N = charter.TN + charter.FP
    print(simulation, charter.FP / N, charter.TP / P,  charter.TP, charter.FP, charter.TN, charter.FN)

